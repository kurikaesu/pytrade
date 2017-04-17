from .broker_base import BrokerBase
from .lightstream import *

from ..instrument import *
from ...core.candle import *

import tkinter as tk
import tkinter.ttk as ttk

import requests
import json

class IGMarkets_config(tk.Frame):
    def __init__(self, igMarketObject, parent=None):
        super(IGMarkets_config, self).__init__(parent)
        self.parent = parent
        self.igMarketObject = igMarketObject

        self.endpointLabel = tk.Label(self, text="Account Type")
        self.endpointLabel.grid(column=0, row=0)

        comboVals = ['Live', 'Demo']
        self.endpointCombo = ttk.Combobox(self, values=comboVals)
        self.endpointCombo.grid(column=1, row=0)

        self.apiKeyLabel = tk.Label(self, text="IG API Key")
        self.apiKeyLabel.grid(column=0, row=1)
        self.apiKeyValue = tk.Entry(self)
        self.apiKeyValue.grid(column=1, row=1)

        self.apiUsernameLabel = tk.Label(self, text="Username/Identifier")
        self.apiUsernameLabel.grid(column=0, row=2)
        self.apiUsernameValue = tk.Entry(self)
        self.apiUsernameValue.grid(column=1, row=2)

        self.apiPasswordLabel = tk.Label(self, text="Password")
        self.apiPasswordLabel.grid(column=0, row=3)
        self.apiPasswordValue = tk.Entry(self, show="*")
        self.apiPasswordValue.grid(column=1, row=3)

        self.testCredentialsButton = tk.Button(self, text="Test", command=self.testCredentials)
        self.testCredentialsButton.grid(column=0, row=4)

        self.testCredentialsResponseString = tk.StringVar()
        self.testCredentialsResponseLabel = tk.Label(self, textvariable=self.testCredentialsResponseString)
        self.testCredentialsResponseLabel.grid(column=0, row=5, columnspan=2)

        self.acceptButton = tk.Button(self, text="Accept", command=self.accept)
        self.acceptButton.grid(column=1, row=4)

        self.cancelButton = tk.Button(self, text="Cancel", command=self.cancel)
        self.cancelButton.grid(column=2, row=4)

        self.pack()

    def testCredentials(self):
        self.igMarketObject.setEndpoint(self.endpointCombo.get())
        authParams = {}
        authParams['api_key'] = self.apiKeyValue.get()
        authParams['identifier'] = self.apiUsernameValue.get()
        authParams['password'] = self.apiPasswordValue.get()

        if self.igMarketObject.authenticate(authParams):
            self.testCredentialsResponseString.set("Success")
        else:
            self.testCredentialsResponseString.set("Failed")

    def accept(self):
        self.igMarketObject.startStream()
        self.parent.destroy()

    def cancel(self):
        self.parent.destroy()

class IGStream():
    def __init__(self, endpoint, identifier, cst, token):
        self.client = LightStreamClient(endpoint, "DEFAULT", identifier, "CST-" + cst + "|XST-" + token)
        self.client.connect()

    def subscribe(self, mode, symbols, fields, callback, page):
        subscription = LightStreamSubscription(
                mode=mode,
                items=symbols,
                fields=fields,
                adapter="DEFAULT"
            )

        subscription.addListener(callback)
        subscription.setOwnerPage(page)
        return self.client.subscribe(subscription)

    def unsubscribe(self, subscriptionId):
        self.client.unsubscribe(subscriptionId)

class IGMarkets(BrokerBase):
    def __init__(self):
        super(IGMarkets, self).__init__("IG Markets")
        self.endpointPrefix = {'Live': 'https://api.ig.com/gateway/deal',
                'Demo': "https://demo-api.ig.com/gateway/deal"}
        self.endpoint = None

        self.requiredAuthParams = {'api_key': 'string', 'identifier': 'string',
                'password': 'password'}

        self.clientId = None
        self.accountId = None
        self.timezoneOffset = None
        self.lightstreamerEndpoint = None
        self.access_token = None
        self.refresh_token = None
        self.token_type = None
        self.cst = None
        self.security_token = None

        self.authResponseFunc = {200: self.authSuccess, 403: self.authFailed}
        self.refreshResponseFunc = {200: self.refreshSuccess}

        self._stream = None

    def setEndpoint(self, endpoint):
        self.endpoint = self.endpointPrefix[endpoint]

    def getRequiredAuthParams(self):
        return self.requiredAuthParams

    def authenticate(self, authParams):
        self.apiKey = authParams['api_key']
        # Let's get the CST and X-SECURITY-TOKEN first
        payload = {'identifier': authParams['identifier'],
                'password': authParams['password']}

        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'VERSION': '3',
            'X-IG-API-KEY': self.apiKey}
        
        r = requests.post(self.endpoint + "/session", headers=headers, data=json.dumps(payload))
        return self.authResponseFunc[r.status_code](r.json())

    def setOauthTokens(self, oauth):
        self.access_token = oauth['access_token']
        self.refresh_token = oauth['refresh_token']
        self.token_type = oauth['token_type']

    def setSessionTokens(self, tokens):
        self.cst = tokens['CST']
        self.security_token = tokens['X-SECURITY-TOKEN']

    def authSuccess(self, response):
        self.clientId = response['clientId']
        self.accountId = response['accountId']
        self.timezoneOffset = response['timezoneOffset']
        self.lightstreamerEndpoint = response['lightstreamerEndpoint']
        self.setOauthTokens(response['oauthToken'])
        self.getCstTokens()

        return True

    def authFailed(self, response):
        return False

    def refreshAccess(self):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Authorization': self.token_type + ' ' + self.access_token,
            'X-IG-API-KEY': self.apiKey,
            'IG-ACCOUNT-ID': self.accountId}

        payload = {'refresh_token': self.refresh_token}

        r = requests.post(self.endpoint + "/session/refresh-token", headers=headers, data=json.dumps(payload))
        self.refreshResponseFunc[r.status_code](r.json())

    def refreshSuccess(self, response):
        self.setOauthTokens(response)

    def getCstTokens(self):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Authorization': self.token_type + ' ' + self.access_token,
            'X-IG-API-KEY': self.apiKey,
            'IG-ACCOUNT-ID': self.accountId}

        r = requests.get(self.endpoint + "/session?fetchSessionTokens=true", headers=headers)
        self.setSessionTokens(r.headers)

    def startStream(self):
        self._stream = IGStream(self.lightstreamerEndpoint, self.accountId, self.cst, self.security_token)

    def getAccountSubscriptionFields(self):
        return ["PNL", "DEPOSIT", "AVAILABLE_CASH", "PNL_LR", "PNL_NLR", "FUNDS", "MARGIN", "MARGIN_LR", "MARGIN_NLR", "AVAILABLE_TO_DEAL", "EQUITY", "EQUITY_USED"]

    def getOrderBookSubscriptionFields(self):
        return ["MID_OPEN", "BID", "OFFER", "HIGH", "LOW", "CHANGE", "CHANGE_PCT", "UPDATE_TIME", "MARKET_DELAY", "MARKET_STATE", "STRIKE_PRICE", "ODDS"]

    def getTradeSubscriptionFields(self):
        return ["CONFIRMS", "OPU", "WOU"]

    def getChartSubscriptionFields(self):
        return ["LTV", "TTV", "UTM", "DAY_OPEN_MID", "DAY_NET_CHG_MID", "DAY_PERC_CHG_MID", "DAY_HIGH", "DAY_LOW", "OFR_OPEN", "OFR_HIGH", "OFR_LOW", "OFR_CLOSE", "BID_OPEN", "BID_HIGH", "BID_LOW", "BID_CLOSE", "LTP_OPEN", "LTP_HIGH", "LTP_LOW", "LTP_CLOSE", "CONS_END", "CONS_TICK_COUNT"]

    def subscribeSymbols(self, page, symbols, fields, callback):
        if page in ["DEPTH", "DEPTH_CHART"]:
            return self._stream.subscribe("MERGE", symbols, fields, callback, page)

    def unsubscribeSymbols(self, subscriptionToken):
        self._stream.unsubscribe(subscriptionToken)

    def findInstrument(self, searchString):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'X-IG-API-KEY': self.apiKey,
            'X-SECURITY-TOKEN': self.security_token,
            'CST': self.cst}
        r = requests.get(self.endpoint + "/markets", headers=headers, params={"searchTerm": searchString})
        temp = json.loads(r.content)
        result = []
        for market in temp["markets"]:
            result.append(Instrument(market["epic"], market["instrumentName"], 
                bid=market["bid"],
                ask=market["offer"], 
                high=market["high"], 
                low=market["low"], 
                netChange=market["netChange"],
                percentChange=market["percentageChange"]))
        return result

    def getInstrument(self, instrumentName):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Version': '3',
            'X-IG-API-KEY': self.apiKey,
            'X-SECURITY-TOKEN': self.security_token,
            'CST': self.cst}

        r = requests.get(self.endpoint + "/markets/" + instrumentName, headers=headers)
        temp = json.loads(r.content)

        instDict = temp["instrument"]
        snapshotDict = temp["snapshot"]

        return Instrument(instDict["epic"], instDict["name"], 
            bid=snapshotDict["bid"], 
            ask=snapshotDict["offer"],
            high=snapshotDict["high"], 
            low=snapshotDict["low"], 
            netChange=snapshotDict["netChange"], 
            pecentChange=snapshotDict["percentageChange"],
            currency=instDict["currencies"][0]["code"])

    def getInstrumentPrices(self, instrumentName, resolution="DAY", _from=None, _to=None):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Version': '3',
            'X-IG-API-KEY': self.apiKey,
            'X-SECURITY-TOKEN': self.security_token,
            'CST': self.cst}

        params = {"resolution": resolution}
        if _from != None:
            params["from"] = _from

        if _to != None:
            params["to"] = _to

        r = requests.get(self.endpoint + "/prices/" + instrumentName, headers=headers, params=params)
        temp = json.loads(r.content)
        for price in temp["prices"]:
            print(price["closePrice"]["ask"])
            
        candles = []
        return candles

    def dealEntry(self, dma, instrument, price, size, direction, orderType, stopLoss, takeProfit):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Version': '2',
            'X-IG-API-KEY': self.apiKey,
            'X-SECURITY-TOKEN': self.security_token,
            'CST': self.cst}

        if dma == False: #OTC
            payload = {"currencyCode": instrument.currency,
                "direction": "BUY" if direction=="LONG" else "SELL",
                "orderType": orderType,
                "epic": instrument.apiName,
                "expiry": "20-APR-17",
                "level": price,
                "size": size,
                "dealReference": "abc123",
                "forceOpen": True,
                "guaranteedStop": False}

            if stopLoss != None:
                payload["forceOpen"] = True
                payload["stopLevel"] = stopLoss

            r = requests.post(self.endpoint + "/positions/otc", headers=headers, data=json.dumps(payload))
            temp = json.loads(r.content)
            print(temp)
            return temp["dealReference"]

    def closeEntry(self, dma, instrument, price, size, direction, orderType, stopLoss, takeProfit):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Version': '1',
            'X-IG-API-KEY': self.apiKey,
            'X-SECURITY-TOKEN': self.security_token,
            'CST': self.cst,
            "_method": "DELETE"}

        if dma == False:
            payload = {
                "epic": instrument.apiName,
                "direction": "BUY" if direction=="LONG" else "SELL",
                "orderType": orderType,
                "expiry": "20-APR-17",
                "size": size
                }

            if orderType == "LIMIT":
                payload["level"] = price

            r = requests.post(self.endpoint + "/positions/otc", headers=headers, data=json.dumps(payload))
            print(r.content)

    def dealWorkingOrder(self, dma, instrument, price, size, direction, orderType, stopLoss, takeProfit, expirationType):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Version': '2',
            'X-IG-API-KEY': self.apiKey,
            'X-SECURITY-TOKEN': self.security_token,
            'CST': self.cst}

        if dma == False:
            tif = ""
            if expirationType=="Good For Day":
                tif = "GOOD_TILL_DATE"
            elif expirationType=="Good Until Cancelled":
                tif = "GOOD_TILL_CANCELLED"
            payload = {
                "currencyCode": instrument.currency,
                "direction": "BUY" if direction=="LONG" else "SELL",
                "epic": instrument.apiName,
                "expiry": "20-APR-17",
                "level": price,
                "size": size,
                "type": orderType,
                "stopLevel": stopLoss,
                "guaranteedStop": False,
                "timeInForce": tif
            }

            if tif == "GOOD_TILL_DATE":
                payload["goodTillDate"] = "2017/04/20 00:00:00"

            r = requests.post(self.endpoint + "/workingorders/otc", headers=headers, data=json.dumps(payload))
            temp = json.loads(r.content)
            print(temp)
            return temp["dealReference"]

    def closeWorkingOrder(self, dma, dealId):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Version': '1',
            'X-IG-API-KEY': self.apiKey,
            'X-SECURITY-TOKEN': self.security_token,
            'CST': self.cst,
            "_method": "DELETE"}

        if dma == False:
            r = requests.post(self.endpoint + "/workingorders/otc/" + dealId, headers=headers)
            print(r.content)

    def showConfig(self, parent):
        IGMarkets_config(self, parent)

# Instantiate this class
IGMarkets()