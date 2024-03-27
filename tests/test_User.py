import unittest
from unittest.mock import MagicMock
from classes.User import User, UserManager

class TestUser(unittest.TestCase):

    def test_is_email_valid_true(self):
        user1 = User("valid@example.com", "123")
        user2 = User("v@e.c", "123")
        user3 = User("loooooong.email.address@with.many.subdomains.info", "123")
        self.assertTrue(user1.is_email_valid())
        self.assertTrue(user2.is_email_valid())
        self.assertTrue(user3.is_email_valid())

    def test_is_email_valid_falsel(self):
        user1 = User("invalid-email", "123")
        user2 = User("invalid-email@with_at", "123")
        self.assertFalse(user1.is_email_valid())
        self.assertFalse(user2.is_email_valid())

    def test_is_password_valid_true(self):
        user1 = User("valid@example.com", "12345678")
        user2 = User("valid@example.com", "AllChars0123456789.?!")
        self.assertTrue(user1.is_password_valid())
        self.assertTrue(user2.is_password_valid())

    def test_is_password_valid_false(self):
        user1 = User("valid@example.com", "short")
        user2 = User("valid@example.com", "forbidden-+=´")
        self.assertFalse(user1.is_password_valid())
        self.assertFalse(user2.is_password_valid())


class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.db_mock = MagicMock()
        self.user_manager = UserManager(self.db_mock)

    def test_save(self):
        user = User("user@example.com", "123")
        self.user_manager.save(user)
        self.db_mock.execute.assert_called_once()

    def test_get_details(self):
        user_id = 1
        self.user_manager.get_details(user_id)
        self.db_mock.execute.assert_called_once_with("SELECT * FROM users WHERE user_id = ?", user_id)

    def test_delete(self):
        user_id = 1
        self.user_manager.delete(user_id)
        self.db_mock.execute.assert_called_once_with("DELETE FROM users WHERE user_id = ?", user_id)


if __name__ == '__main__':
    unittest.main()