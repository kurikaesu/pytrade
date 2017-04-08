import tkinter as tk
import tkinter.ttk as ttk

class Candle:
    def __init__(self):
        self._timestamp = None
        self._open = None
        self._high = None
        self._low = None
        self._close = None

    def timestamp(self):
        return self._timestamp

    def setTimestamp(self, newTimestamp=None):
        self._timestamp = newTimestamp

    def open(self):
        return self._open

    def setOpen(self, newOpen=None):
        self._open = newOpen

    def high(self):
        return self._high

    def setHigh(self, newHigh=None):
        self._high = newHigh

    def low(self):
        return self._low

    def setLow(self, newLow=None):
        self._low = newLow

    def close(self):
        return self._close

    def setClose(self, newClose=None):
        self._close = newClose

    def lastPrint(self, lastPrint=None):
        if lastPrint == None:
            return # Maybe throw an exception

        if self._close == None:
            self._open = self._high = self._low = self._close = lastPrint
            return

        self._close = lastPrint

        if lastPrint > self._high:
            self._high = lastPrint

        if lastPrint < self._low:
            self._low = lastPrint


class Chart:
    def __init__(self):
        self._candles = []
        self._candleGroupSize = 1
        self._aggregateCandles = []

        self._startingTimestamp = None # Should be from when the symbol starts

    def setGroupSize(self, newGroupSize=1):
        self._candleGroupSize = newGroupSize

    def processPrint(self, lastPrint=None):
        if lastPrint == None:
            pass #This should throw an exception
