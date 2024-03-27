from flask import flash, redirect, request, session, url_for
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/3.0.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You have to log in or sign up.")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


def redirect_url(default="index"):
    """Redirect url to the previous page"""
    return request.args.get("next") or \
           request.referrer or \
           url_for(default)