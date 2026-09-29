from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, flash, redirect, render_template, session, url_for
from werkzeug.utils import secure_filename

from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import StudentProfile, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def allowed_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_ID_EXTENSIONS"]


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        if User.query.filter_by(email=email).first():
            flash("That email is already registered.", "danger")
            return render_template("auth/register.html", form=form)

        uploaded = form.valid_id.data
        if not uploaded or not allowed_extension(uploaded.filename):
            flash("Invalid ID file type.", "danger")
            return render_template("auth/register.html", form=form)

        original_name = secure_filename(uploaded.filename)
        if not original_name:
            flash("Invalid file name.", "danger")
            return render_template("auth/register.html", form=form)

        extension = Path(original_name).suffix.lower()
        stored_name = f"{uuid4().hex}{extension}"
        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        upload_folder.mkdir(parents=True, exist_ok=True)
        uploaded.save(upload_folder / stored_name)

        user = User(email=email, role="student")
        user.set_password(form.password.data)

        profile = StudentProfile(
            user=user,
            full_name=form.full_name.data.strip(),
            contact_number=form.contact_number.data.strip(),
            course_program=form.course_program.data.strip(),
            address=form.address.data.strip(),
            id_original_name=original_name,
            id_stored_name=stored_name,
            id_mime_type=uploaded.mimetype or "application/octet-stream",
        )

        db.session.add(user)
        db.session.add(profile)
        db.session.commit()

        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(form.password.data):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", form=form)

        session.clear()
        session["user_id"] = user.id
        session["role"] = user.role
        session.permanent = True

        if user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.post("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))
