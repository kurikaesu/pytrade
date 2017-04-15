from .broker_base import BrokerBase
from .lightstream import *

import tkinter as tk
import tkinter.ttk as ttk

import requests
import json

class IGMarkets_config(tk.Frame):
    def __init__(self, igMarketObject, parent=None):
        super(IGMarkets_config, self).__init__(parent)
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

        self.pack()

    def testCredentials(self):
        self.igMarketObject.setEndpoint(self.endpointCombo.get())
        authParams = {}
        authParams['api_key'] = self.apiKeyValue.get()
        authParams['identifier'] = self.apiUsernameValue.get()
        authParams['password'] = self.apiPasswordValue.get()

        if self.igMarketObject.authenticate(authParams):
            self.testCredentialsResponseString.set("Success")
            self.igMarketObject.startStream()
        else:
            self.testCredentialsResponseString.set("Failed")

class IGStream():
    def __init__(self, endpoint, identifier, cst, token):
        self.client = LightStreamClient(endpoint, "DEFAULT", identifier, "CST-" + cst + "|XST-" + token)
        self.client.connect()

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

    def showConfig(self, parent):
        IGMarkets_config(self, parent)

# Instantiate this class
IGMarkets()