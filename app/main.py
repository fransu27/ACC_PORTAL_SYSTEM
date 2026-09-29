from flask import Blueprint, flash, redirect, render_template, session, url_for

from app import db
from app.decorators import login_required
from app.forms import ScholarshipApplicationForm
from app.models import Scholarship, ScholarshipApplication, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    user = db.session.get(User, session["user_id"])
    applications = ScholarshipApplication.query.filter_by(
        student_id=user.id
    ).order_by(ScholarshipApplication.submitted_at.desc()).all()

    return render_template(
        "student/dashboard.html",
        user=user,
        applications=applications,
    )


@main_bp.route("/scholarships/apply", methods=["GET", "POST"])
@login_required
def apply_scholarship():
    user = db.session.get(User, session["user_id"])
    scholarships = Scholarship.query.filter_by(active=True).order_by(Scholarship.name).all()

    form = ScholarshipApplicationForm()
    form.scholarship_id.choices = [(s.id, s.name) for s in scholarships]

    if form.validate_on_submit():
        scholarship = db.session.get(Scholarship, form.scholarship_id.data)

        if not scholarship or not scholarship.active:
            flash("That scholarship is no longer available.", "danger")
            return redirect(url_for("main.apply_scholarship"))

        existing = ScholarshipApplication.query.filter_by(
            student_id=user.id,
            scholarship_id=scholarship.id,
        ).first()

        if existing:
            flash("You have already applied for this scholarship.", "warning")
            return redirect(url_for("main.dashboard"))

        application = ScholarshipApplication(
            student_id=user.id,
            scholarship_id=scholarship.id,
        )
        db.session.add(application)
        db.session.commit()

        flash("Scholarship application submitted.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template(
        "student/apply.html",
        form=form,
        scholarships=scholarships,
    )
