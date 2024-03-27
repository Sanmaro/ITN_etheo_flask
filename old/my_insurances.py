from datetime import datetime

from flask import flash, redirect, request, url_for


def get_insurance_details(db, insurance_id=None, client_id=None, user_rights=None):
    """Get information about an insurance plan"""
    base_query = """SELECT i.*, 
                           (insuree_client.first_name || " " || insuree_client.second_name) AS insuree_full_name, 
                           (policyholder_client.first_name || " " || policyholder_client.second_name) AS policyholder_full_name 
                    FROM insurances AS i
                    INNER JOIN clients AS insuree_client ON i.insuree = insuree_client.client_id
                    INNER JOIN clients AS policyholder_client ON i.policyholder = policyholder_client.client_id"""
    if user_rights == 1:
        insurances = db.execute(f"{base_query}")
    elif insurance_id:
        insurances = db.execute(f"{base_query} WHERE i.insurance_id=?", insurance_id)[0]
    elif client_id:
        insurances = db.execute(f"{base_query} WHERE insuree=? OR policyholder=?", client_id, client_id)
    return insurances
    

def get_insurance_types():
    """List all available types of an insurance plan"""
    insurance_types = [
        ("life", "Life"), 
        ("travel", "Travel"), 
        ("car", "Car")
        ]
    return insurance_types


def write_into_insurances(db, query, user_id, insurance_id=None):
    """Update or insert an insurance plan into the database"""
    type = request.form.get("insurance_type")
    amount = request.form.get("insurance_amount")
    date = datetime.now()
    policyholder = db.execute("SELECT client_id FROM clients WHERE user=?", user_id)[0]["client_id"]
    try:
        insuree_first, insuree_second = request.form.get("insurance_insuree").split()
        insuree = db.execute("SELECT client_id FROM clients WHERE first_name=? AND second_name=?", insuree_first, insuree_second)[0]["client_id"]
        
        # Obtain a new insurance plan
        if query.startswith("INSERT"):
            db.execute(query,
                    type, amount, insuree, policyholder, date)
            flash("You have purchased a new insurance plan.")

        # Update the existing insurance plan
        elif query.startswith("UPDATE"):
            db.execute(query,
                       type, amount, insuree, insurance_id)
            flash("You have updated the insurance plan.")
        return redirect(url_for("my_insurances"))
    
    except (ValueError, IndexError):
        flash("This client is not in our register")
        return redirect(url_for("my_insurances"))