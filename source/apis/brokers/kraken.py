from .broker_base import *

from ..instrument import *

import requests
import json

class Kraken(BrokerBase):
    def __init__(self):
        super(Kraken, self).__init__("Kraken")
        self.endpoint = "https://api.kraken.com/0/"
        self._assetPairs = {}

    def _retrieveAssetPairs(self):
        r = requests.get(self.endpoint + "/public/AssetPairs")
        temp = json.loads(r.content)
        for k, v in temp["result"].items():
            self._assetPairs[k] = v

    def findInstrument(self, searchString):
        self._retrieveAssetPairs()
        result = []
        for k, v in self._assetPairs.items():
            if searchString in k or searchString in v["altname"]:
                result.append(Instrument(v["altname"], k))

        return result

    def getInstrument(self, instrumentName):
        self._retrieveAssetPairs()
        instDict = self._assetPairs[instrumentName]
        return Instrument(instDict["altname"], instrumentName)

#instantiate this broker
Kraken()