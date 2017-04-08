#from .broker_base import BrokerBase
import requests
import json

#class IGMarkets(BrokerBase):
class IGMarkets:
    def __init__(self):
        #super(IGMarkets, self).__init__(self)
        self.endpointPrefix = {'live': 'https://api.ig.com/gateway/deal',
                'demo': "https://demo-api.ig.com/gateway/deal"}

        self.requiredAuthParams = {'api_key': 'string', 'identifier': 'string',
                'password': 'password'}

        self.clientId = None
        self.accountId = None
        self.timezoneOffset = None
        self.lightstreamerEndpoint = None
        self.access_token = None
        self.refresh_token = None
        self.token_type = None

        self.authResponseFunc = {200: self.authSuccess, 403: self.authFailed}
        self.refreshResponseFunc = {200: self.refreshSuccess}

    def getRequiredAuthParams(self):
        return self.requiredAuthParams

    def authenticate(self, authParams):
        self.apiKey = authParams['api_key']
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'VERSION': '3',
            'X-IG-API-KEY': self.apiKey}

        payload = {'identifier': authParams['identifier'],
                'password': authParams['password']}

        r = requests.post(self.endpointPrefix + "/session", headers=headers, data=json.dumps(payload))
        self.authResponseFunc[r.status_code](r.json())

    def setOauthTokens(self, oauth):
        self.access_token = oauth['access_token']
        self.refresh_token = oauth['refresh_token']
        self.token_type = oauth['token_type']

    def authSuccess(self, response):
        self.clientId = response['clientId']
        self.accountId = response['accountId']
        self.timezoneOffset = response['timezoneOffset']
        self.lightstreamerEndpoint = response['lightstreamerEndpoint']
        self.setOauthTokens(response['oauthToken'])

    def authFailed(self, response):
        print("Auth failed")

    def refreshAccess(self):
        headers = {'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'Authorization': self.token_type + ' ' + self.access_token,
            'X-IG-API-KEY': self.apiKey,
            'IG-ACCOUNT-ID': self.accountId}

        payload = {'refresh_token': self.refresh_token}

        r = requests.post(self.endpointPrefix + "/session/refresh-token", headers=headers, data=json.dumps(payload))
        self.refreshResponseFunc[r.status_code](r.json())

    def refreshSuccess(self, response):
        self.setOauthTokens(response)
