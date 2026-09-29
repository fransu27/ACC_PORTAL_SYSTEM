from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


PHONE_RE = r"^[0-9+\-\s()]{7,30}$"


class RegistrationForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
    )
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=150)],
    )
    contact_number = StringField(
        "Contact Number",
        validators=[DataRequired(), Regexp(PHONE_RE, message="Enter a valid contact number.")],
    )
    course_program = StringField(
        "Course / Program",
        validators=[DataRequired(), Length(min=2, max=150)],
    )
    address = TextAreaField(
        "Address",
        validators=[DataRequired(), Length(min=5, max=500)],
    )
    valid_id = FileField(
        "Valid ID",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png", "pdf"], "Only JPG, JPEG, PNG, and PDF files are allowed."),
        ],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ScholarshipApplicationForm(FlaskForm):
    scholarship_id = SelectField("Scholarship", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit Application")


class ReviewApplicationForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Rejected", "Rejected"),
        ],
        validators=[DataRequired()],
    )
    admin_note = TextAreaField("Admin Note", validators=[Length(max=1000)])
    submit = SubmitField("Save Review")
