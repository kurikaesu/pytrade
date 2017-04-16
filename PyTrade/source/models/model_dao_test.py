import unittest
import os
import sqlite3

from .model_dao import ModelDAO
from .user import User



class TestModelDAOClass(unittest.TestCase):
    username = b'bush@gmail.com'
    password = b'abc123'
    user = User(username)
    user.set_password()
    user.save_data()

    def test_save_object(self):

        dao = ModelDAO(None)
        dao.save_object(self.user)
        #self.assertTrue(True, dao.save_object(self.user))

    def test_get_max_id(self):

        db = sqlite3.connect('TestModelDAO.db')
        dao = ModelDAO(db)
        self.user.save_data()

    def __connectDB(self):
        return sqlite3.connect('TestModelDAO.db')

    def __destroyDB(self):
        os.remove('TestModelDAO.db')

