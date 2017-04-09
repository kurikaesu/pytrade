
#  Copyright (c) Lightstreamer Srl.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# Modified by Aren Villanueva <arenvillanueva.at.yomogi-soft.com>
# Original source available at:
# https://github.com/Lightstreamer/Lightstreamer-example-StockList-client-python/blob/master/src/stock_list_demo.py

import requests

class LightStreamClient():
	def __init__(self, base_url, adapter_set="", user="", password=""):
		self._base_url = base_url
		self._adapter_set = adapter_set
		self._user = user
		self._password = password
		self._session = {}
		self._subscriptions = {}
		self._current_subscription_key = 0
		self._stream_connection = None
		self._stream_connection_thread = None
		self._bind_counter = 0

	def connect(self):
		payload = {"LS_op2": "create",
			"LS_cid": "mgQkwtwdysogQz2BJ4Ji kOj2Bg",
			"LS_adapter_set": self._adapter_set,
			"LS_user": self._user,
			"LS_password": self._password}
		r = requests.post(self._base_url + "/lightstreamer/create_session.txt", data=payload, stream=True)
		return r.status_code == 200