import unittest
from .user import User


class TestUserClass(unittest.TestCase):

    def test_user_creation_with_password(self):

        username = b'bush@gmail.com'
        password = b'ABC123'
        incorrect_pw = b'ACB123'
        user = User(username)
        user.set_password(password)
        # User is correctly created
        self.assertEqual(username, user.get_username())
        # Validate user password, should get True
        self.assertTrue(user.validate_password(password))
        # Validate user password, should get False
        self.assertFalse(user.validate_password(incorrect_pw))
