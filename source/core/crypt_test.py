import unittest

from .crypt import Crypt

class CryptTest(unittest.TestCase):
    def setUp(self):
        self.c = Crypt()
        self.salt = b'\xdb\xa5\x9e\x06he\xb5^\xbdO\xac"\xe0\x02\xcaa'

    def testCreation(self):
        c = Crypt()
        self.assertTrue(c != None)

    def testNewSalt(self):
        self.assertFalse(self.c.newSalt() == None)

    def testSetSalt(self):
        self.c.setSalt(self.salt)
        self.assertTrue(self.c._salt == self.salt)

    def testInitialisation(self):
        self.c.setSalt(self.c.newSalt())
        self.c.initWithPassword(b'ABC')
        self.assertTrue(self.c._f != None)

    def testEncryption(self):
        self.c.setSalt(self.salt)
        self.c.initWithPassword(b'ABC123')
        text = b"This is some sample text"
        res = self.c.encryptBytes(text)
        res2 = self.c.decryptBytes(res)
        self.assertTrue(res2 == text)
