
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
import threading

class LightStreamSubscription:
	def __init__(self, mode, items, fields, adapter=""):
		self.item_names = items
		self._items_map = {}
		self.field_names = fields
		self.adapter = adapter
		self.mode = mode
		self.snapshot = "true"
		self._listeners = []

	def _decode(self, value, last):
		if value == "$":
			return u''
		elif value == "#":
			return None
		elif not value:
			return last
		elif value[0] in "#$":
			value = value[1:]

		return value

	def addListener(self, listener):
		self._listeners.append(listener)

	def notifyUpdate(self, item_line):
		toks = item_line.rstrip('\r\n').split('|')

class LightStreamClient():
	PROBE_CMD = b"PROBE"
	END_CMD = b"END"
	LOOP_CMD = b"LOOP"
	ERROR_CMD = b"ERROR"
	SYNC_ERROR_CMD = b"SYNC ERROR"
	OK_CMD = b"OK"
	PREAMBLE_CMD = b"Preamble"
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
		self._iterLines = None
		self._control_url = self._base_url

	def _readFromStream(self):
		return self._iterLines.__next__()

	def _handleStream(self, streamLine):
		if streamLine == LightStreamClient.OK_CMD:
			while True:
				nextStreamLine = self._readFromStream()
				if nextStreamLine:
					sessionKey, sessionValue = nextStreamLine.split(b":", 1)
					self._session[sessionKey] = sessionValue
				else:
					break

			self._setControlLinkUrl(self._session.get(b"ControlAddress"))

			self._stream_connection_thread = threading.Thread(
					name="STREAM_CONN_THREAD-{0}".format(self._bind_counter),
					target=self._receive
				)

			self._stream_connection_thread.setDaemon(True)
			self._stream_connection_thread.start()
		else:
			pass # We got an unknown response. Handle it here

	def _setControlLinkUrl(self, customAddress=None):
		if customAddress != None:
			pass

	def _receive(self):
		rebind = False
		receive = True
		while receive:
			try:
				message = self._readFromStream()
			except Exception:
				print("Something went wrong")
				message = None

			print(message)

			if message is None:
				receive = False
			elif message == LightStreamClient.PROBE_CMD:
				pass # Probably just a heartbeat
			elif message.startsWith(LightStreamClient.ERROR_CMD):
				receive = False
			elif message.startsWith(LightStreamClient.LOOP_CMD):
				receive = False
				rebind = True
			elif message.startsWith(LightStreamClient.SYNC_ERROR_CMD):
				receive = False
			elif message.startsWith(LightStreamClient.END_CMD):
				receive = False
			elif message.startsWith(LightStreamClient.PREAMBLE_CMD):
				pass #do nothing
			else:
				self._forwardUpdateMessage(message)

		if not rebind:
			self._stream_connection.close()
			self._stream_connection = None
			self._session.clear()
			self._subscriptions.clear()
			self._current_subscription_key = 0

	def connect(self):
		payload = {"LS_op2": "create",
			"LS_cid": "mgQkwtwdysogQz2BJ4Ji kOj2Bg",
			"LS_adapter_set": self._adapter_set,
			"LS_user": self._user,
			"LS_password": self._password}
		self._stream_connection = requests.post(self._base_url + "/lightstreamer/create_session.txt", data=payload, stream=True)
		self._iterLines = self._stream_connection.iter_lines()
		self._handleStream(self._readFromStream())

	def subscribe(self, subscription):
		self._current_subscription_key += 1
		self._subscriptions[self._current_subscription_key] = subscription

		return self._current_subscription_key

	def unsubscribe(self, subscription_key):
		pass

	def _forwardUpdateMessage(self, updateMessage):
		tok = updateMessage.split(',')
		table, item = int(tok[0]), tok[1]
		if table in self._subscriptions:
			self._subscriptions[table].notifyUpdate(item)
		else:
			pass # no subscription found