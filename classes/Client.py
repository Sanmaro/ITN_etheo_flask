class Client:
    """Represent a client in the database"""
    def __init__(self, first, second, birthdate, phone, street, street_no, city, country, zip, user_id=None):
        self.first_name = first
        self.second_name = second
        self.birthdate = birthdate
        self.phone = phone
        self.street = street
        self.street_no = street_no
        self.city = city
        self.country = country
        self.zip_code = zip
        self.user_id = user_id


class ClientManager:
    """Data access layer for the Client class"""
    def __init__(self, db):
        self.db = db

    def delete(self, user_id):
        """Remove a client from the database"""
        deleted = self.db.execute("DELETE FROM users WHERE user_id=?", user_id)
        return deleted

    def exists(self, user_id):
        """Check if a client record exists for the given user_id."""
        result = self.db.execute("SELECT 1 FROM clients WHERE user = ?", user_id)
        return result
    
    def get_details(self, user_id=None):
        """Retrieve client details from the database"""
        if user_id:
            try:
                client = self.db.execute("SELECT c.*, u.user_id, u.email, u.rights FROM clients AS c INNER JOIN users AS u ON u.user_id=c.user WHERE u.user_id=?", user_id)[0]
            except IndexError:
                self.save_empty_client(user_id)
                client = self.db.execute("SELECT c.*, u.user_id, u.email, u.rights FROM clients AS c INNER JOIN users AS u ON u.user_id=c.user WHERE u.user_id=?", user_id)[0]
        else:
            client = self.db.execute("SELECT c.*, u.user_id, u.email, u.rights FROM users AS u LEFT JOIN clients AS c ON u.user_id=c.user")
        return client
    
    def get_full_name(self, user_id):
        """Return the full name of the client."""
        client_data = self.get_details(user_id=user_id)
        return f"{client_data["first_name"]} {client_data["second_name"]}"

    def save(self, client):
        """Insert a new client into the database."""
        saved = self.db.execute("INSERT INTO clients (first_name, second_name, birthdate, phone, street, street_no, city, country, zip, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", client.first_name, client.second_name, client.birthdate, client.phone, client.street, client.street_no, client.city, client.country, client.zip_code, client.user_id)
        return saved

    def save_empty_client(self, user_id):
        default = ""
        self.db.execute("INSERT INTO clients (first_name, second_name, birthdate," 
                    "phone, street, street_no, city, country, zip, user)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    default, default, default, default, default, default,
                    default, default, default, user_id)
        
    def update(self, client):
        """Update client information in the database."""
        updated = self.db.execute("UPDATE clients SET first_name = ?, second_name = ?, birthdate = ?, phone = ?, street = ?, street_no = ?, city = ?, country = ?, zip = ? WHERE user = ?", client.first_name, client.second_name, client.birthdate, client.phone, client.street, client.street_no, client.city, client.country, client.zip_code, client.user_id)
        return updated
    
