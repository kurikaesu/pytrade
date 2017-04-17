
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

from ..instrument import *
from ..chart_data import *

class LightStreamSubscription:
	def __init__(self, mode, items, fields, adapter=""):
		self.item_names = items
		self._items_map = {}
		self.field_names = fields
		self.adapter = adapter
		self.mode = mode
		self.snapshot = "true"
		self._listeners = []
		self._subscriptionOwnerPage = None
		self._interval = "SECOND"

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

	def setOwnerPage(self, desc):
		self._subscriptionOwnerPage = desc

	def setInterval(self, interval):
		self._interval = interval

	def notifyUpdate(self, item_line):
		toks = item_line.rstrip('\r\n').split('|')
		undecodedItem = dict(list(zip(self.field_names, toks[1:])))

		itemPos = int(toks[0])
		currentItem = self._items_map.get(itemPos, {})

		self._items_map[itemPos] = dict([
				(k, self._decode(v, currentItem.get(k))) for k, v in list(undecodedItem.items())
			])

		itemInfo = {
			"pos": itemPos,
			"name": self.item_names[itemPos -1],
			"values": self._items_map[itemPos]
		}

		#print(itemInfo)

		returnedItem = None

		if self._subscriptionOwnerPage == "DEPTH":
			returnedItem = Instrument(self.item_names[itemPos - 1], self.item_names[itemPos - 1],
					bid=self._items_map[itemPos]["BID"],
					ask=self._items_map[itemPos]["OFFER"],
					high=self._items_map[itemPos]["HIGH"],
					low=self._items_map[itemPos]["LOW"],
					percentChange=self._items_map[itemPos]["CHANGE"])
		elif self._subscriptionOwnerPage == "DEPTH_CHART":
			closePrice = self._items_map[itemPos]["LTP_CLOSE"]
			if closePrice == "":
				closePrice = self._items_map[itemPos]["BID_CLOSE"] + "|" + self._items_map[itemPos]["OFR_CLOSE"]
			returnedItem = ChartData(self.item_names[itemPos - 1],
					lastTradedVolume=self._items_map[itemPos]["LTV"],
					updateTime=self._items_map[itemPos]["UTM"],
					dayOpen=self._items_map[itemPos]["DAY_OPEN_MID"],
					netChange=self._items_map[itemPos]["DAY_NET_CHG_MID"],
					percentChange=self._items_map[itemPos]["DAY_PERC_CHG_MID"],
					dayHigh=self._items_map[itemPos]["DAY_HIGH"],
					dayLow=self._items_map[itemPos]["DAY_LOW"],
					lastClose=closePrice)

		for onItemUpdate in self._listeners:
			try:
				onItemUpdate(returnedItem)
			except AttributeError:
				pass

class LightStreamClient():
	CONNECTION_URL_PATH = "lightstreamer/create_session.txt"
	BIND_URL_PATH = "lightstreamer/bind_session.txt"
	CONTROL_URL_PATH = "lightstreamer/control.txt"

	OP_ADD = "add"
	OP_DELETE = "delete"
	OP_DESTROY = "destroy"

	PROBE_CMD = "PROBE"
	END_CMD = "END"
	LOOP_CMD = "LOOP"
	ERROR_CMD = "ERROR"
	SYNC_ERROR_CMD = "SYNC ERROR"
	OK_CMD = "OK"
	PREAMBLE_CMD = "Preamble"
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
		return self._iterLines.__next__().decode("utf-8")

	def _handleStream(self, streamLine):
		if streamLine == LightStreamClient.OK_CMD:
			while True:
				nextStreamLine = self._readFromStream()
				if nextStreamLine:
					sessionKey, sessionValue = nextStreamLine.split(":", 1)
					self._session[sessionKey] = sessionValue
				else:
					break

			self._setControlLinkUrl(self._session.get("ControlAddress"))

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
			self._control_url = "%s//%s" % (self._base_url.split('/')[0], customAddress)

	def _receive(self):
		rebind = False
		receive = True
		while receive:
			try:
				message = self._readFromStream()
			except Exception:
				print("Something went wrong")
				message = None

			#print(message)

			if message is None:
				receive = False
			elif message == LightStreamClient.PROBE_CMD:
				pass # Probably just a heartbeat
			elif message.startswith(LightStreamClient.ERROR_CMD):
				receive = False
			elif message.startswith(LightStreamClient.LOOP_CMD):
				receive = False
				rebind = True
			elif message.startswith(LightStreamClient.SYNC_ERROR_CMD):
				receive = False
			elif message.startswith(LightStreamClient.END_CMD):
				receive = False
			elif message.startswith(LightStreamClient.PREAMBLE_CMD):
				pass #do nothing
			else:
				self._forwardUpdateMessage(message)

		if not rebind:
			self._stream_connection.close()
			self._stream_connection = None
			self._session.clear()
			self._subscriptions.clear()
			self._current_subscription_key = 0
		else:
			self.bind()

	def _control(self, params):
		if self._session.get("SessionId") == None:
			print("Session not ready")
			return

		params["LS_session"] = self._session["SessionId"]
		r = requests.post(self._control_url + '/' + LightStreamClient.CONTROL_URL_PATH, data=params)
		return r.content

	def _join(self):
		if self._stream_connection_thread:
			self._stream_connection_thread.join()
			self._stream_connection_thread = None

	def bind(self):
		self._stream_connection = requests.post(self._base_url + '/' + LightStreamClient.BIND_URL_PATH, data={"LS_session": self._session["SessionId"]})
		self._bind_counter += 1
		self._handleStream(self._readFromStream())

	def connect(self):
		payload = {"LS_op2": "create",
			"LS_cid": "mgQkwtwdysogQz2BJ4Ji kOj2Bg",
			"LS_adapter_set": self._adapter_set,
			"LS_user": self._user,
			"LS_password": self._password}
		self._stream_connection = requests.post(self._base_url + '/' + LightStreamClient.CONNECTION_URL_PATH, data=payload, stream=True)
		self._iterLines = self._stream_connection.iter_lines()
		self._handleStream(self._readFromStream())

	def disconnect(self):
		if self._stream_connection is not None:
			self._stream_connection.close()
		else:
			pass # No connection to lightstreamer

	def destroy(self):
		if self._stream_connection is not None:
			serverResponse = self._control({"LS_op": LightStreamClient.OP_DESTROY})
			if serverResponse == LightStreamClient.OK_CMD:
				self._join()
			else:
				pass # No connection to lighstreamer

	def subscribe(self, subscription):
		self._current_subscription_key += 1
		self._subscriptions[self._current_subscription_key] = subscription

		itemList = []
		if subscription.mode == "MERGE":
			if subscription._subscriptionOwnerPage == "DEPTH":
				for itemName in subscription.item_names:
					itemList.append("MARKET:" + itemName)
			elif subscription._subscriptionOwnerPage == "DEPTH_CHART":
				for itemName in subscription.item_names:
					itemList.append("CHART:" + itemName + ":" + subscription._interval)

		response = self._control({
			"LS_Table": self._current_subscription_key,
			"LS_op": LightStreamClient.OP_ADD,
			"LS_data_adapter": subscription.adapter,
			"LS_mode": subscription.mode,
			"LS_schema": " ".join(subscription.field_names),
			"LS_id": " ".join(itemList),
			})

		return self._current_subscription_key

	def unsubscribe(self, subscription_key):
		if subscription_key in self._subscriptions:
			serverResponse = self._control({
				"LS_Table": subscription_key,
				"LS_op": LightStreamClient.OP_DELETE
				})

			if serverResponse == LightStreamClient.OK_CMD:
				del self._subscriptions[subscription_key]
			else:
				pass # Server error
		else:
			pass # Unknown subscription key

	def _forwardUpdateMessage(self, updateMessage):
		tok = updateMessage.split(',')
		table, item = int(tok[0]), tok[1]
		if table in self._subscriptions:
			self._subscriptions[table].notifyUpdate(item)
		else:
			pass # no subscription found