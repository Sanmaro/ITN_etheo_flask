import unittest
from unittest.mock import MagicMock
from classes.Client import Client, ClientManager  # Adjust the import as needed

class TestClient(unittest.TestCase):
    def test_client_initialization(self):
        client = Client("John", "Doe", "1990-01-01", "123456789", "Main Street", "42", "Springfield", "USA", "12345", 1)
        self.assertEqual(client.first_name, "John")
        self.assertEqual(client.second_name, "Doe")
        self.assertEqual(client.birthdate, "1990-01-01")
        self.assertEqual(client.phone, "123456789")
        self.assertEqual(client.street, "Main Street")
        self.assertEqual(client.street_no, "42")
        self.assertEqual(client.city, "Springfield")
        self.assertEqual(client.country, "USA")
        self.assertEqual(client.zip_code, "12345")
        self.assertEqual(client.user_id, 1)

class TestClientManager(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.client_manager = ClientManager(self.db)
        self.test_client = Client("John", "Doe", "1990-01-01", "123456789", "Main Street", "42", "Springfield", "USA", "12345", 1)

    def test_save(self):
        self.client_manager.save(self.test_client)
        self.db.execute.assert_called_once()

    def test_update(self):
        self.client_manager.update(self.test_client)
        self.db.execute.assert_called_once_with("UPDATE clients SET first_name = ?, second_name = ?, birthdate = ?, phone = ?, street = ?, street_no = ?, city = ?, country = ?, zip = ? WHERE user = ?", self.test_client.first_name, self.test_client.second_name, self.test_client.birthdate, self.test_client.phone, self.test_client.street, self.test_client.street_no, self.test_client.city, self.test_client.country, self.test_client.zip_code, self.test_client.user_id)  

    def test_delete(self):
        self.client_manager.delete(self.test_client.user_id)
        self.db.execute.assert_called_once_with("DELETE FROM users WHERE user_id=?", self.test_client.user_id)

    def test_exists(self):
        self.client_manager.exists(self.test_client.user_id)
        self.db.execute.assert_called_once_with("SELECT 1 FROM clients WHERE user = ?", self.test_client.user_id)

    def test_get_details(self):
        self.client_manager.get_details(self.test_client.user_id)
        self.db.execute.assert_called_once_with("SELECT c.*, u.user_id, u.email, u.rights FROM clients AS c INNER JOIN users AS u ON u.user_id=c.user WHERE u.user_id=?", self.test_client.user_id)  

    def test_get_full_name(self):
        self.client_manager.db.execute.return_value = [{"first_name": "John", "second_name": "Doe"}]
        full_name = self.client_manager.get_full_name(self.test_client.user_id)
        self.assertEqual(full_name, "John Doe")

if __name__ == '__main__':
    unittest.main()
