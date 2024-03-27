import re

from flask import flash, redirect, url_for
from werkzeug.security import generate_password_hash


def check_user_email(email):
    """Check if user entered a valid e-mail (intermediate checker)"""
    regex_email = re.fullmatch(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
                                   r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
                                   r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
                                     email)
    return regex_email


def check_user_pass(password, password_conf):
    """Check if user entered a valid password (at least 8 characters)"""
    if password:
        # regex_pass = re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{4,}$", 
        #                         password)
        regex_pass = re.fullmatch(r"[a-zA-Z0-9]{8,}", password)
        if not regex_pass:
            flash("Your password is too short (enter at least 8 characters).")
            return None
        if password != password_conf:
            flash("The passwords are not identical.")
            return None
        password_hash = generate_password_hash(password)
        return password_hash
    

def get_user_details(db, user_id):
    """Get all information about the user"""
    user = db.execute("SELECT * FROM users WHERE user_id=?", user_id)[0]
    return user


def write_into_users(db, query, user_id):
    """Delete the user"""
    if query.startswith("DELETE"):
        db.execute(query, 
                   user_id)
    return redirect(url_for("my_clients"))