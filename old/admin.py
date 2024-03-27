def admin_get_client_details(db, user_id=None):
    """Get all data about the client and everything about the user except for password hash"""
    if user_id:
        client = db.execute("SELECT c.*, u.user_id, u.email, u.rights FROM clients AS c INNER JOIN users AS u ON u.user_id=c.user WHERE u.user_id=?", user_id)[0]
    else:
        client = db.execute("SELECT c.*, u.user_id, u.email, u.rights FROM users AS u LEFT JOIN clients AS c ON u.user_id=c.user")
    return client