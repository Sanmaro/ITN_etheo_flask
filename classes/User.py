import re

from werkzeug.security import generate_password_hash


class User:
    """Represent a user in the database"""
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def is_email_valid(self):
        """Check if user entered a valid e-mail (intermediate checker)"""
        regex_email = re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                                        self.email)
        return regex_email

    def is_password_valid(self):
        """Check if user entered a valid password (at least 8 characters)"""
        regex_pass = re.fullmatch(r"[a-zA-Z0-9.?!]{8,}", self.password)
        return regex_pass
       

class UserManager:
    """Data access layer for the User class"""
    def __init__(self, db):
        self.db = db
    
    def save(self, user):
        """Insert the user into the database"""
        password_hash = generate_password_hash(user.password)
        self.db.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                user.email, password_hash)

    def get_details(self, user_id):
        """Retrieve all data related to a user from the database."""
        user = self.db.execute("SELECT * FROM users WHERE user_id = ?", user_id)[0]
        return user

    def delete(self, user_id):
        """Delete a user from the database."""
        self.db.execute("DELETE FROM users WHERE user_id = ?", user_id)

