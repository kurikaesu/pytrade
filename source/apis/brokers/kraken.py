from .broker_base import *

from ..instrument import *

import requests
import json
import time
import threading

class Kraken(BrokerBase):
    def __init__(self):
        super(Kraken, self).__init__("Kraken")
        self.endpoint = "https://api.kraken.com/0/"
        self._assetPairs = {}
        self._subscriptionThreads = {}
        self._currentSubscriptions = 0
        self._waitTiers = {"0": 30, "1": 15}
        self._myTier = "0"

    def _retrieveAssetPairs(self):
        r = requests.get(self.endpoint + "/public/AssetPairs")
        temp = json.loads(r.content)
        for k, v in temp["result"].items():
            self._assetPairs[k] = v

    def _streamPair(self, pair, subscriptionToken, callback):
        lastId = None
        params = {"pair": pair}
        myInstrument = self.getInstrument(pair[0])
        rate = self._waitTiers[self._myTier]
        counter = 0
        while self._subscriptionThreads[subscriptionToken][0]:
            if counter >= rate:
                counter = 0
                try:
                    if lastId != None:
                        params["since"] = lastId
                    r = requests.get(self.endpoint + "/public/OHLC", params=params)
                    temp = json.loads(r.content)
                    prices = temp["result"][pair[0]]
                    lastPrint = prices[len(prices)-1]

                    if lastId != temp["result"]["last"]:
                        myInstrument.open=lastPrint[1]
                        myInstrument.high=lastPrint[2]
                        myInstrument.low=lastPrint[3]
                        myInstrument.close=lastPrint[4]
                        myInstrument.vwap=lastPrint[5]
                        myInstrument.lastVolume=lastPrint[6]
                        closePrice = float(lastPrint[4])
                        myInstrument.netChange=closePrice-myInstrument.dayOpen
                        percentChange = ((100.0 / myInstrument.dayOpen) * closePrice) - 100.0
                        myInstrument.percentChange=percentChange

                    lastId = temp["result"]["last"]
                except KeyError:
                    print(r.content)

                try:
                    r = requests.get(self.endpoint + "/public/Depth", params={"pair": pair})
                    temp = json.loads(r.content)
                    print(r.content)
                except KeyError:
                    print(r.content)

            else:
                counter += 1

            myInstrument.nextRefresh=rate-counter
            callback(myInstrument)

            time.sleep(1)


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
        return Instrument(instDict["altname"], instrumentName, 
            bid=resultDict["b"][0], 
            ask=resultDict["a"][0], 
            high=resultDict["h"][0], 
            low=resultDict["l"][0], 
            netChange=netChange, 
            percentChange=percentChange,
            dayOpen=openPrice,
            _open=openPrice, 
            _close=closePrice,
            bidSize=resultDict["b"][2], 
            askSize=resultDict["a"][2], 
            vwap=resultDict["p"][0], 
            lastVolume=resultDict["c"][1], 
            exchange="KRAKEN")

    def subscribeSymbols(self, symbols, fields, callback):
        self._currentSubscriptions += 1
        self._subscriptionThreads[self._currentSubscriptions] = [True, threading.Thread(name="KRAKEN_STREAM-{0}".format(self._currentSubscriptions), 
            target=self._streamPair, args=(symbols, self._currentSubscriptions, callback))]
        self._subscriptionThreads[self._currentSubscriptions][1].setDaemon(True)
        self._subscriptionThreads[self._currentSubscriptions][1].start()


    def unsubscribeSymbols(self, subscriptionToken):
        self._subscriptionThreads[subscriptionToken][0] = False

#instantiate this broker
Kraken()