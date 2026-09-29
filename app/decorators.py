from functools import wraps

from flask import abort, session


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            from flask import flash, redirect, url_for
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login", next=request_path()))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            from flask import flash, redirect, url_for
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("role") != "admin":
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def request_path():
    from flask import request
    return request.full_path
