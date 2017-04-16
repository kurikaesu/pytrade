brokerPluginList = {}

class BrokerBase:
    def __init__(self, name):
        brokerPluginList[name] = self

    def authenticate(self, authParams=None):
        pass

    def showConfig(self, parent=None):
        pass

    def findInstrument(self, searchString):
        return []

    def getInstrument(self, instrumentName):
        return None

    def getInstrumentPrices(self, instrumentName, resolution="DAY", _from=None, _to=None):
        return None

    def subscribeSymbols(self, symbols, fields, callback):
        pass

    def unsubscribeSymbols(self, subscriptionToken):
        pass