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
            raise ValueError("The last print value cannot be None")

        if self._close == None:
            self._open = self._high = self._low = self._close = lastPrint
            return

        self._close = lastPrint

        if lastPrint > self._high:
            self._high = lastPrint

        if lastPrint < self._low:
            self._low = lastPrint
            