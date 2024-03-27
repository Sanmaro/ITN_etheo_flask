from flask import flash, redirect, request, url_for
from utils.utils import redirect_url


def get_client_details(db, user_id=None):
    """Get all information about the client"""
    try:
        client = db.execute("SELECT * FROM clients WHERE user=?", user_id)[0]
    except IndexError:
        default = ""
        db.execute("INSERT INTO clients (first_name, second_name, birthdate," 
                    "phone, street, street_no, city, country, zip, user)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    default, default, default, default, default, default,
                    default, default, default, user_id)
        client = db.execute("SELECT * FROM clients WHERE user=?", user_id)[0]
    return client


def get_client_id_and_username(db, user_id):
    """Get client_id and full name"""
    client = get_client_details(db, user_id)
    client_id = client["client_id"]
    username = " ".join([client["first_name"], client["second_name"]])
    return client_id, username


def write_into_clients(db, user_id=None):
    """Update or insert a client into the database"""
    first = request.form.get("signup_client_first")
    second = request.form.get("signup_client_second")
    birthdate = request.form.get("signup_client_birthdate")
    phone = request.form.get("signup_client_phone")
    street = request.form.get("signup_client_street")
    street_no = request.form.get("signup_client_street_no")
    city = request.form.get("signup_client_city")
    country = request.form.get("signup_client_country")
    zip = request.form.get("signup_client_zip")

    # Updating existing client
    if user_id:
        db.execute("""UPDATE clients
SET first_name = ?, second_name = ?, birthdate = ?,
    phone = ?, street = ?, street_no = ?, city = ?, country = ?, zip = ?
WHERE user = ? AND (
    first_name != ? OR second_name != ? OR birthdate != ? OR
    phone != ? OR street != ? OR street_no != ? OR city != ? OR
    country != ? OR zip != ?
)""", 
                first, second, birthdate, phone, street, street_no, city, country, zip, 
                user_id,
                first, second, birthdate, phone, street, street_no, city, country, zip)
        flash("You have successfully updated your personal information.")
        return redirect(redirect_url())
    
    # Registering a new client
    else:
        user = db.execute("SELECT MAX(user_id) FROM users")[0]["MAX(user_id)"]

        db.execute("INSERT INTO clients (first_name, second_name, birthdate," 
                    "phone, street, street_no, city, country, zip, user)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    first, second, birthdate, 
                phone, street, street_no, city, country, zip, user)
        flash("You have successfuly signed up as a client. Please, log in.")
        return redirect(url_for("login"))