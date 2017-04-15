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
        r = requests.get(self.endpoint + "/public/Ticker", params={"pair": instDict["altname"]})
        temp = json.loads(r.content)
        resultDict = temp["result"][instDict["altname"]]
        openPrice = float(resultDict["o"])
        closePrice = float(resultDict["c"][0])
        netChange = closePrice - openPrice
        percentChange = ((100.0 / openPrice) * closePrice) - 100.
        return Instrument(instDict["altname"], instrumentName, resultDict["b"][0], 
            resultDict["a"][0], resultDict["h"][0], resultDict["l"][0], netChange, percentChange, openPrice, closePrice,
            resultDict["b"][2], resultDict["a"][2], resultDict["p"][0], resultDict["c"][1], "KRAKEN")

#instantiate this broker
Kraken()