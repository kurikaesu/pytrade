class Instrument:
    def __init__(self, apiName=0.0, name=0.0, **kwargs):
        self.apiName = apiName
        self.name = name
        self.dayOpen = kwargs.get("dayOpen", 0.0)
        self.open = kwargs.get("_open", 0.0)
        self.close = kwargs.get("_close", 0.0)
        self.bid = kwargs.get("bid", 0.0)
        self.bidSize = kwargs.get("bidSize", 0.0)
        self.ask = kwargs.get("ask", 0.0)
        self.askSize = kwargs.get("askSize", 0.0)
        self.high = kwargs.get("high", 0.0)
        self.low = kwargs.get("low", 0.0)
        self.netChange = kwargs.get("netChange", 0.0)
        self.percentChange = kwargs.get("percentChange", 0.0)
        self.vwap = kwargs.get("vwap", 0.0)
        self.lastVolume = kwargs.get("lastVolume", 0.0)
        self.exchange = kwargs.get("exchange", 0.0)
        self.nextRefresh = kwargs.get("nextRefresh", "N/A")
        self.bidDepth = []
        self.askDepth = []
