from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, abort, current_app, flash, redirect, render_template, send_from_directory, url_for

from app import db
from app.decorators import admin_required
from app.forms import ReviewApplicationForm
from app.models import Scholarship, ScholarshipApplication, StudentProfile, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def dashboard():
    students = User.query.filter_by(role="student").order_by(User.created_at.desc()).all()
    applications = ScholarshipApplication.query.order_by(
        ScholarshipApplication.submitted_at.desc()
    ).all()
    return render_template(
        "admin/dashboard.html",
        students=students,
        applications=applications,
    )


@admin_bp.route("/students")
@admin_required
def students():
    students = User.query.filter_by(role="student").order_by(User.created_at.desc()).all()
    return render_template("admin/students.html", students=students)


@admin_bp.route("/students/<int:user_id>/id")
@admin_required
def view_student_id(user_id):
    user = db.session.get(User, user_id)
    if not user or not user.student:
        abort(404)

    profile = user.student
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])

    return send_from_directory(
        upload_folder,
        profile.id_stored_name,
        as_attachment=False,
        mimetype=profile.id_mime_type,
    )


@admin_bp.route("/applications/<int:application_id>/review", methods=["GET", "POST"])
@admin_required
def review_application(application_id):
    application = db.session.get(ScholarshipApplication, application_id)
    if not application:
        abort(404)

    form = ReviewApplicationForm(obj=application)

    if form.validate_on_submit():
        application.status = form.status.data
        application.admin_note = form.admin_note.data.strip() if form.admin_note.data else None
        application.reviewed_at = datetime.now(timezone.utc)
        db.session.commit()

        flash("Application review saved.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/review_application.html",
        application=application,
        form=form,
    )


@admin_bp.post("/setup-scholarships")
@admin_required
def setup_scholarships():
    if Scholarship.query.count() == 0:
        db.session.add_all(
            [
                Scholarship(
                    name="ACC Academic Scholarship",
                    description="For students who meet the academic scholarship criteria.",
                ),
                Scholarship(
                    name="ACC Financial Assistance Scholarship",
                    description="For qualified students who need financial assistance.",
                ),
            ]
        )
        db.session.commit()
        flash("Sample scholarships created.", "success")
    else:
        flash("Scholarships already exist.", "info")

    return redirect(url_for("admin.dashboard"))