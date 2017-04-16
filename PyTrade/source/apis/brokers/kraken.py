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
        self._subscriptionThread = None
        self._currentSubscriptions = {}
        self._subscriptionInstruments = {}
        self._waitTiers = {"0": 30, "1": 15}
        self._myTier = "0"
        self._subscriptionCount = 0
        self._subscriptionPairs = {}

    def _retrieveAssetPairs(self):
        r = requests.get(self.endpoint + "/public/AssetPairs")
        temp = json.loads(r.content)
        for k, v in temp["result"].items():
            self._assetPairs[k] = v

    def _streamPair(self):
        lastId = None
        rate = self._waitTiers[self._myTier]
        counter = 0
        while True:
            if counter >= rate:
                counter = 0
                keys = []
                for k, v in self._currentSubscriptions.items():
                    keys.append(k)

                params={"pair": ",".join(keys)}
                
                if lastId != None:
                    params["since"] = lastId

                r = requests.get(self.endpoint + "/public/OHLC", params=params)
                ohlcResponse = json.loads(r.content)

                r = requests.get(self.endpoint + "/public/Depth", params=params)
                depthResponse = json.loads(r.content)

                r = requests.get(self.endpoint + "/public/Trades", params=params)
                tapeResponse = json.loads(r.content)

                if "result" in ohlcResponse:
                    if lastId != ohlcResponse["result"]["last"]:
                        for instrumentName in ohlcResponse["result"]:
                            if instrumentName != "last":
                                instrument = ohlcResponse["result"][instrumentName]
                                lastPrint=instrument[len(instrument)-1]
                                if instrumentName not in self._subscriptionInstruments:
                                    self._subscriptionInstruments[instrumentName] = self.getInstrument(instrumentName)

                                self._subscriptionInstruments[instrumentName].open=lastPrint[1]
                                self._subscriptionInstruments[instrumentName].high=lastPrint[2]
                                self._subscriptionInstruments[instrumentName].low=lastPrint[3]
                                self._subscriptionInstruments[instrumentName].close=lastPrint[4]
                                self._subscriptionInstruments[instrumentName].vwap=lastPrint[5]
                                self._subscriptionInstruments[instrumentName].lastVolume=lastPrint[6]
                                closePrice = float(lastPrint[4])
                                percentChange = ((100.0/self._subscriptionInstruments[instrumentName].dayOpen)*closePrice) - 100.0
                                self._subscriptionInstruments[instrumentName].netChange=closePrice - self._subscriptionInstruments[instrumentName].dayOpen
                                self._subscriptionInstruments[instrumentName].percentChange=percentChange

                    lastId = ohlcResponse["result"]["last"]

                if "result" in depthResponse:
                    for instrumentName in depthResponse["result"]:
                        if instrumentName in self._subscriptionInstruments:
                            self._subscriptionInstruments[instrumentName].bidDepth = depthResponse["result"][instrumentName]["bids"]
                            self._subscriptionInstruments[instrumentName].askDepth = depthResponse["result"][instrumentName]["asks"]

                            self._subscriptionInstruments[instrumentName].bid = depthResponse["result"][instrumentName]["bids"][0][0]
                            self._subscriptionInstruments[instrumentName].bidSize = depthResponse["result"][instrumentName]["bids"][0][1]
                            self._subscriptionInstruments[instrumentName].ask = depthResponse["result"][instrumentName]["asks"][0][0]
                            self._subscriptionInstruments[instrumentName].askSize = depthResponse["result"][instrumentName]["asks"][0][1]

                if "result" in tapeResponse:
                    for instrumentName in tapeResponse["result"]:
                        if instrumentName in self._subscriptionInstruments:
                            self._subscriptionInstruments[instrumentName].tapeDepth = tapeResponse["result"][instrumentName]

                else:
                    print("Rate is too low. Increasing by 5 seconds")
                    rate += 5
            else:
                counter += 1

            for k, v in self._currentSubscriptions.items():
                if k not in self._subscriptionInstruments:
                    self._subscriptionInstruments[k] = self.getInstrument(k)

                instrument = self._subscriptionInstruments[k]
                instrument.nextRefresh=rate-counter

                for onUpdate in v:
                    onUpdate(instrument)

            time.sleep(1)

    def findInstrument(self, searchString):
        self._retrieveAssetPairs()
        result = []
        for k, v in self._assetPairs.items():
            if searchString in k or searchString in v["altname"]:
                result.append(Instrument(k, v["altname"]))

        return result

    def getInstrument(self, instrumentName):
        self._retrieveAssetPairs()
        instDict = self._assetPairs[instrumentName]
        r = requests.get(self.endpoint + "/public/Ticker", params={"pair": instDict["altname"]})
        temp = json.loads(r.content)
        resultDict = temp["result"][instrumentName]
        openPrice = float(resultDict["o"])
        closePrice = float(resultDict["c"][0])
        netChange = closePrice - openPrice
        percentChange = ((100.0 / openPrice) * closePrice) - 100.

        r = requests.get(self.endpoint + "/public/Depth", params={"pair": instDict["altname"]})
        temp = json.loads(r.content)
        depth = temp["result"][instrumentName]

        r = requests.get(self.endpoint + "/public/Trades", params={"pair": instDict["altname"]})
        temp = json.loads(r.content)
        tape = temp["result"][instrumentName]
        return Instrument(instrumentName, instDict["altname"],
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
            exchange="KRAKEN",
            bidDepth=depth["bids"],
            askDepth=depth["asks"],
            tapeDepth=tape)

    def subscribeSymbols(self, symbols, fields, callback):
        for symbol in symbols:
            if symbol not in self._currentSubscriptions:
                self._currentSubscriptions[symbol] = []

            self._currentSubscriptions[symbol].append(callback)

        self._subscriptionCount += 1
        self._subscriptionPairs[self._subscriptionCount] = [symbols, callback]
        
        if self._subscriptionThread == None:
            self._subscriptionThread = threading.Thread(name="KRAKEN_STREAM-THREAD", 
            target=self._streamPair)

            self._subscriptionThread.setDaemon(True)
            self._subscriptionThread.start()

        return self._subscriptionCount

    def unsubscribeSymbols(self, subscriptionToken):
        for symbol, pair in self._currentSubscriptions.items():
            if symbol in self._subscriptionPairs[subscriptionToken][0]:
                if self._subscriptionPairs[subscriptionToken][1] in self._currentSubscriptions[symbol]:
                    self._currentSubscriptions[symbol].remove(self._subscriptionPairs[subscriptionToken][1])

                    if len(self._currentSubscriptions[symbol]) == 0:
                        del self._currentSubscriptions[symbol]

                    break

        del self._subscriptionPairs[subscriptionToken]


#instantiate this broker
Kraken()