from datetime import datetime

import logging


class Insurance:
    """Represent an insurance plan in the database"""
    def __init__(self, type, amount, insuree, policyholder, insurance_id=None):
        self.insurance_id = insurance_id
        self.type = type
        self.amount = amount
        self.insuree = insuree
        self.policyholder = policyholder
        self.date = datetime.today()

    @staticmethod
    def get_types():
        """List all available types of an insurance plan"""
        return [
            ("life", "Life"),
            ("travel", "Travel"),
            ("car", "Car")
        ]


class InsuranceManager:
    def __init__(self, db):
        self.db = db

    def delete(self, insurance_id):
        deleted = self.db.execute("DELETE FROM insurances WHERE insurance_id=?", insurance_id)
        return deleted

    def get_details(self, insurance_id=None, client_id=None, user_rights=None):
        """Retrieve details about insurance plans from the database."""
        base_query = """SELECT i.*, 
                               (insuree_client.first_name || " " || insuree_client.second_name) AS insuree_full_name, 
                               (policyholder_client.first_name || " " || policyholder_client.second_name) AS policyholder_full_name 
                        FROM insurances AS i
                        INNER JOIN clients AS insuree_client ON i.insuree = insuree_client.client_id
                        INNER JOIN clients AS policyholder_client ON i.policyholder = policyholder_client.client_id"""
        if user_rights == 1:
            return self.db.execute(f"{base_query}")
        elif insurance_id:
            return self.db.execute(f"{base_query} WHERE i.insurance_id=?", insurance_id)[0]
        elif client_id:
            return self.db.execute(f"{base_query} WHERE insuree=? OR policyholder=?", client_id, client_id)

    def save(self, insurance):
        try:
            self.db.execute("INSERT INTO insurances (type, amount, insuree, policyholder, date) VALUES (?, ?, ?, ?, ?)",
                                    insurance.type, insurance.amount, insurance.insuree, insurance.policyholder, insurance.date)
            return True
        except Exception as e:
            logging.error(f"An error occurred while saving the insurance plan: {e}")
            return False

    def update(self, insurance):
        """Update an insurance plan in the database."""
        try:
            self.db.execute("UPDATE insurances SET type=?, amount=?, insuree=? WHERE insurance_id=?", insurance.type, insurance.amount, insurance.insuree, insurance.insurance_id)
            return True
        except Exception as e:
            logging.error(f"An error occurred while updating the insurance plan: {e}")
            return False
    
