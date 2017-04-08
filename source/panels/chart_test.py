import unittest
from .chart import *

class TestCandleMethods(unittest.TestCase):
    def setUp(self):
        self.candle = Candle()

    def test_creation(self):
        c = Candle()
        self.assertFalse(c == None)
        self.assertTrue(c._timestamp == c._open == c._high == c._low == c._close == None)

    def test_lastPrint(self):
        self.candle.lastPrint(1.0)
        self.assertTrue(self.candle._open == 1.0)
        self.candle.lastPrint(2.0)
        self.assertTrue(self.candle._high == 2.0)
        self.assertTrue(self.candle._open == 1.0)
        self.candle.lastPrint(3.0)
        self.assertTrue(self.candle._high == 3.0)
        self.candle.lastPrint(0.5)
        self.assertTrue(self.candle._high == 3.0)
        self.assertTrue(self.candle._low == 0.5)
        self.candle.lastPrint(0.7)
        self.assertTrue(self.candle._close == 0.7)
        self.assertTrue(self.candle._low == 0.5)
        self.assertTrue(self.candle._high == 3.0)
        self.assertTrue(self.candle._open == 1.0)
