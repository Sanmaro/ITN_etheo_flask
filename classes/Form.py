
from flask import request

class FormManager:
    def __init__(self, db):
        self.db = db

    def extract_insurance(self, user_id):
        """Extract insurance data from the form"""
        type = request.form.get("insurance_type")
        amount = request.form.get("insurance_amount")
        try:
            insuree_first, insuree_second = request.form.get("insurance_insuree").split()
            insuree = self.db.execute("SELECT client_id FROM clients WHERE first_name=? AND second_name=?", insuree_first, insuree_second)[0]["client_id"]
        except (ValueError, IndexError):
            insuree = ""
        policyholder = self.db.execute("SELECT client_id FROM clients WHERE user=?", user_id)[0]["client_id"]
        return {"type": type, "amount": amount, "insuree": insuree, "policyholder": policyholder}

    @staticmethod
    def extract_client():
        """Extract client data from the form."""
        form_keys = ["first", "second", "birthdate", "phone", "street", "street_no", "city", "country", "zip"]
        return {key: request.form.get(f"signup_client_{key}") for key in form_keys}
    
    @staticmethod
    def extract_user():
        """Extract user data from the form"""
        form_keys = ["email", "password", "password_conf"]
        return {key: request.form.get(f"signup_{key}") for key in form_keys}
    
    @staticmethod
    def extract_event():
        form_keys = ["description", "date", "location"]
        event_data = {key: request.form.get(f"event_{key}") for key in form_keys}
        event_data["document"] = request.files["event_documents"]
        return event_data
    
    @staticmethod
    def extract_contact_message():
        form_keys = ["name", "email", "message"]
        return {key: request.form.get(f"contact_{key}") for key in form_keys}