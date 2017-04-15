class Instrument:
    def __init__(self, apiName=0.0, name=0.0, bid=0.0, ask=0.0, high=0.0, low=0.0, netChange=0.0, percentChange=0.0, _open=0.0, _close=0.0, bidSize=0.0, askSize=0.0, vwap=0.0, lastVolume=0.0, exchange=""):
        self.apiName = apiName
        self.name = name
        self.open = _open
        self.close = _close
        self.bid = bid
        self.bidSize = bidSize
        self.ask = ask
        self.askSize = askSize
        self.high = high
        self.low = low
        self.netChange = netChange
        self.percentChange = percentChange
        self.vwap = vwap
        self.lastVolume = lastVolume
        self.exchange = exchange

        if self.netChange == None:
            self.netChange = 0.0

        if self.percentChange == None:
            self.percentChange = 0.0