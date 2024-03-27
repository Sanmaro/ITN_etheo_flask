from datetime import datetime
import unittest
from unittest.mock import MagicMock
from classes.Insurance import Insurance, InsuranceManager

class TestInsurance(unittest.TestCase):

    def setUp(self):
        # Setup an instance of Insurance for use in tests
        self.insurance = Insurance(
            type="life",
            amount=100000,
            insuree="Insuree Name",
            policyholder="Policyholder Name",
            insurance_id=1
        )

    def test_initialization(self):
        # Test that the Insurance instance has been initialized with the correct attributes
        self.assertEqual(self.insurance.type, "life")
        self.assertEqual(self.insurance.amount, 100000)
        self.assertEqual(self.insurance.insuree, "Insuree Name")
        self.assertEqual(self.insurance.policyholder, "Policyholder Name")
        self.assertEqual(self.insurance.date, datetime.today())
        self.assertEqual(self.insurance.insurance_id, 1)

    def test_get_types(self):
        # Test the static method get_types
        types = Insurance.get_types()
        self.assertIn(("life", "Life"), types)
        self.assertIn(("travel", "Travel"), types)
        self.assertIn(("car", "Car"), types)


class TestInsuranceManager(unittest.TestCase):

    def setUp(self):
        # Mock the database connection
        self.db = MagicMock()
        self.insurance_manager = InsuranceManager(self.db)

        # Example insurance data
        self.insurance_data = {
            "type": "life",
            "amount": 100000,
            "insuree": 1,
            "policyholder": 2,
            "insurance_id": 1
        }
        self.insurance = Insurance(**self.insurance_data)

    def test_delete(self):
        insurance_id = 1
        self.insurance_manager.delete(insurance_id)
        self.db.execute.assert_called_once_with("DELETE FROM insurances WHERE insurance_id=?", insurance_id)

    def test_get_details_by_id(self):
        insurance_id = 1
        self.insurance_manager.get_details(insurance_id=insurance_id)
        self.db.execute.assert_called_once()

    def test_get_details_by_client_id(self):
        client_id = 1
        self.insurance_manager.get_details(client_id=client_id)
        self.db.execute.assert_called_once()

    def test_save(self):
        self.insurance_manager.save(self.insurance)
        self.db.execute.assert_called_once_with(
            "INSERT INTO insurances (type, amount, insuree, policyholder, date) VALUES (?, ?, ?, ?, ?)",
            self.insurance.type, self.insurance.amount, self.insurance.insuree, self.insurance.policyholder, self.insurance.date
        )

    def test_update(self):
        self.insurance_manager.update(self.insurance)
        self.db.execute.assert_called_once_with(
            "UPDATE insurances SET type=?, amount=?, insuree=? WHERE insurance_id=?",
            self.insurance.type, self.insurance.amount, self.insurance.insuree, self.insurance.insurance_id
        )


if __name__ == '__main__':
    unittest.main()
