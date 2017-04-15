class MovingAverage:
    def __init__(self, candles=None, period=1, exponential=False):
        self._candles = candles
        self._period = period
        self._exponential = exponential