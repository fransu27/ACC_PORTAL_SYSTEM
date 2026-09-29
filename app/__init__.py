from pathlib import Path

import click
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    from app.models import User  # noqa: F401
    from app.auth import auth_bp
    from app.main import main_bp
    from app.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(413)
    def request_entity_too_large(_error):
        from flask import render_template
        return render_template("error.html", code=413, message="The uploaded file is too large. Maximum size is 5 MB."), 413

    @app.errorhandler(403)
    def forbidden(_error):
        from flask import render_template
        return render_template("error.html", code=403, message="You do not have permission to access this page."), 403

    @app.cli.command("init-db")
    def init_db():
        """Create all database tables."""
        with app.app_context():
            db.create_all()
        click.echo("Database tables created.")

    @app.cli.command("create-admin")
    def create_admin():
        """Create an administrator account interactively."""
        import getpass
        from app.models import User

        email = click.prompt("Admin email").strip().lower()
        password = getpass.getpass("Admin password: ")
        confirm = getpass.getpass("Confirm password: ")

        if password != confirm:
            raise click.ClickException("Passwords do not match.")
        if len(password) < 8:
            raise click.ClickException("Password must contain at least 8 characters.")

        with app.app_context():
            if User.query.filter_by(email=email).first():
                raise click.ClickException("A user with that email already exists.")

            admin = User(email=email, role="admin")
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()

        click.echo(f"Admin account created for {email}.")

    return app
