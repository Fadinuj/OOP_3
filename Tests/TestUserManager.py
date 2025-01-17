import unittest
from unittest.mock import patch, mock_open
from Backend.UserManager import UserManager
from Backend.User import User

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.user_manager.users = []

    def test_add_user(self):
        self.user_manager.add_user("test_user", "password123")
        self.assertEqual(len(self.user_manager.users), 1)
        self.assertEqual(self.user_manager.users[0].username, "test_user")

    @patch("builtins.open", new_callable=mock_open, read_data="username,password_hash,active\n")
    def test_load_users(self, mock_file):
        self.user_manager.load_users()
        self.assertEqual(len(self.user_manager.users), 0)  # Mock CSV has no users

    def test_user_exists(self):
        self.user_manager.add_user("existing_user", "password123")
        self.assertTrue(self.user_manager.user_exists("existing_user"))
        self.assertFalse(self.user_manager.user_exists("nonexistent_user"))

    def test_authenticate_user(self):
        self.user_manager.add_user("test_user", "password123")
        self.assertTrue(self.user_manager.authenticate("test_user", "password123"))
        self.assertFalse(self.user_manager.authenticate("test_user", "wrong_password"))
