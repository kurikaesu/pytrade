class ChartData:
    def __init__(self, name, **kwargs):
        self.name = name
        self.lastTradedVolume = kwargs.get("lastTradedVolume", 0.0)
        self.updateTime = kwargs.get("updateTime", None)
        self.dayOpen = kwargs.get("dayOpen", 0.0)
        self.netChange = kwargs.get("netChange", None)
        self.percentChange = kwargs.get("percentChange", None)
        self.dayHigh = kwargs.get("dayHigh", 0.0)
        self.dayLow = kwargs.get("dayLow", 0.0)
        self.lastClose = kwargs.get("lastClose", None)