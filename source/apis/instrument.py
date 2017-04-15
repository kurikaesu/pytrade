class Instrument:
    def __init__(self, apiName=0.0, name=0.0, bid=0.0, ask=0.0, high=0.0, low=0.0, netChange=0.0, percentChange=0.0):
        self.apiName = apiName
        self.name = name
        self.bid = bid
        self.ask = ask
        self.high = high
        self.low = low
        self.netChange = netChange
        self.percentChange = percentChange

        if self.netChange == None:
            self.netChange = 0.0

        if self.percentChange == None:
            self.percentChange = 0.0