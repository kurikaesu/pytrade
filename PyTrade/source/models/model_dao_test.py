import unittest
import logging
from .model_dao import ModelDAO
from .user import User

logging.basicConfig(level=logging.DEBUG)


class TestModelDAOClass(unittest.TestCase):

    def test_save_object(self):
        log = logging.getLogger("TestModelDAO")
        username = b'bush@gmail.com'
        dao = ModelDAO(None)
        user = User(username)
        dao.save_object(user)

        log.debug('class name : %s' % dao.save_object(user) )
        self.assertTrue(True, dao.save_object(user))
