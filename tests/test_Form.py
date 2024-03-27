import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from classes.Form import FormManager

class TestFormManager(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.db = MagicMock()
        self.form_manager = FormManager(self.db)

    def test_extract_insurance(self):
        with self.app.test_request_context('/path', method='POST', data={
            "insurance_type": "car",
            "insurance_amount": "1000",
            "insurance_insuree": "John Doe"
        }):
            with patch.object(self.form_manager.db, 'execute') as mock_db_execute:
                mock_db_execute.side_effect = lambda query, *args: [{'client_id': 1}] if "first_name" in query else [{'client_id': 2}]
                result = self.form_manager.extract_insurance(user_id=123)
                expected_result = {"type": "car", "amount": "1000", "insuree": 1, "policyholder": 2}
                self.assertEqual(result, expected_result)
                mock_db_execute.assert_called()


    def test_extract_client(self):
        with self.app.test_request_context("/some_route", method="POST", data={
            "signup_client_first": "John",
            "signup_client_second": "Doe",
            "signup_client_birthdate": "1990-01-01",
            "signup_client_phone": "123456789",
            "signup_client_street": "Main Street",
            "signup_client_street_no": "42",
            "signup_client_city": "Springfield",
            "signup_client_country": "USA",
            "signup_client_zip": "12345"
        }):
            client_data = FormManager.extract_client()
            self.assertEqual(client_data["first"], "John")
            self.assertEqual(client_data["second"], "Doe")
            self.assertEqual(client_data["birthdate"], "1990-01-01")
            self.assertEqual(client_data["phone"], "123456789")
            self.assertEqual(client_data["street"], "Main Street")
            self.assertEqual(client_data["street_no"], "42")
            self.assertEqual(client_data["city"], "Springfield")
            self.assertEqual(client_data["country"], "USA")
            self.assertEqual(client_data["zip"], "12345")

    def test_extract_user(self):
        with self.app.test_request_context("/some_route", method="POST", data={
            "signup_email": "john.doe@example.com",
            "signup_password": "securepassword",
            "signup_password_conf": "securepassword"
        }):
            user_data = FormManager.extract_user()
            self.assertEqual(user_data["email"], "john.doe@example.com")
            self.assertEqual(user_data["password"], "securepassword")
            self.assertEqual(user_data["password_conf"], "securepassword")

if __name__ == "__main__":
    unittest.main()
