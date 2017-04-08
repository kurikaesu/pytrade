brokerPluginList = {}

class BrokerBase:
    def __init__(self, name):
        brokerPluginList[name] = self

    def authenticate(self, authParams=None):
        pass

    def showConfig(self, parent=None):
        pass
