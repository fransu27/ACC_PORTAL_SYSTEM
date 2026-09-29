from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


def utcnow():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

    student = db.relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    applications = db.relationship(
        "ScholarshipApplication",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    full_name = db.Column(db.String(150), nullable=False)
    contact_number = db.Column(db.String(30), nullable=False)
    course_program = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text, nullable=False)

    id_original_name = db.Column(db.String(255), nullable=False)
    id_stored_name = db.Column(db.String(255), nullable=False)
    id_mime_type = db.Column(db.String(100), nullable=False)
    id_uploaded_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

    user = db.relationship("User", back_populates="student")


class Scholarship(db.Model):
    __tablename__ = "scholarships"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    applications = db.relationship("ScholarshipApplication", back_populates="scholarship")


class ScholarshipApplication(db.Model):
    __tablename__ = "scholarship_applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    scholarship_id = db.Column(db.Integer, db.ForeignKey("scholarships.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    submitted_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    reviewed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    admin_note = db.Column(db.Text, nullable=True)

    student = db.relationship("User", back_populates="applications")
    scholarship = db.relationship("Scholarship", back_populates="applications")

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "scholarship_id",
            name="uq_student_scholarship",
        ),
    )
