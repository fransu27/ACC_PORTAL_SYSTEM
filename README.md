# ACC Portal System

A Flask + SQLite student registration and scholarship application portal.

## Features

- Student registration and login
- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Student profile and valid ID upload
- Secure upload validation and randomized filenames
- Scholarship applications
- Student application status tracking
- Admin dashboard
- Admin review of student IDs
- Admin approval/rejection of scholarship applications
- SQLAlchemy ORM with a database URL that can later point to PostgreSQL

## Default workflow

1. Create a virtual environment.
2. Install `requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Run `python run.py`.
5. Visit `http://127.0.0.1:5000`.
6. Use the `flask` CLI to create an admin account:

```text
flask --app run.py create-admin
```

The command prompts for the admin email and password.

## Security notes

- Do not commit `.env`.
- Do not store uploads inside `static/`.
- Use HTTPS in production.
- Replace the development secret with a cryptographically random value.
- Consider PostgreSQL for multi-user production deployments.
