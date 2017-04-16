import tkinter as tk
import tkinter.ttk as ttk

import json

class DepthTape(tk.Frame):
    def __init__(self, parent=None, broker=None):
        super(DepthTape, self).__init__(parent)
        self.broker = broker
        self.kekka_map = {}
        self._subscription_token = None
        self._currentSymbol = None
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self._onClose)
        self.grid()

        # Symbol
        self._symbolVar = tk.StringVar()
        self._symbolVar.trace("w", self.symbolTextChanged)
        self.symbolPicker = ttk.Combobox(self, textvariable=self._symbolVar)
        self.symbolPicker.bind("<Return>", self.getInstrument)
        self.symbolPicker.bind("<<ComboboxSelected>>", self.setSubscribedInstrument)
        self.symbolPicker.grid(column=0, row=0, columnspan=3)

        # Last Print
        self.lastPrintLabel = tk.Label(self, text="0.000")
        self.lastPrintLabel.grid(column=4, row=0, columnspan=2)

        # Change
        self._changeLabelVar = tk.DoubleVar()
        self.changeLabel = tk.Label(self, text="0.00", textvariable=self._changeLabelVar)
        self.changeLabel.grid(column=5, row=0)

        # Change %
        self._changePercentVar = tk.StringVar()
        self.changePercentLabel = tk.Label(self, text="0.00%", textvariable=self._changePercentVar)
        self.changePercentLabel.grid(column=6, row=0)

        # Last Volume
        self._lastVolumeLabelVar = tk.DoubleVar()
        self.lastVolumeLabel = tk.Label(self, text="0", textvariable=self._lastVolumeLabelVar)
        self.lastVolumeLabel.grid(column=7, row=0)

        # Next Refresh
        self.nextRefreshLabel = tk.Label(self, text="Next Refresh:")
        self.nextRefreshLabel.grid(column=8, row=0)
        self._nextRefreshValueVar = tk.StringVar()
        self.nextRefreshValue = tk.Label(self, text="N/A", textvariable=self._nextRefreshValueVar)
        self.nextRefreshValue.grid(column=9, row=0)

        # L1 Open
        self.openLabel = tk.Label(self, text="Open")
        self.openLabel.grid(column=0, row=1)
        self._openValueVar = tk.DoubleVar()
        self.openValue = tk.Label(self, text="0.000", textvariable=self._openValueVar)
        self.openValue.grid(column=1, row=1)

        # L1 Close
        self.closeLabel = tk.Label(self, text="Close")
        self.closeLabel.grid(column=2, row=1)
        self._closeValueVar = tk.DoubleVar()
        self.closeValue = tk.Label(self, text="0.000", textvariable=self._closeValueVar)
        self.closeValue.grid(column=3, row=1)

        # L1 Highest
        self.highestLabel = tk.Label(self, text="High")
        self.highestLabel.grid(column=4, row=1)
        self._highestValueVar = tk.DoubleVar()
        self.highestValue = tk.Label(self, text="0.000", textvariable=self._highestValueVar)
        self.highestValue.grid(column=5, row=1)

        # L1 Lowest
        self.lowestLabel = tk.Label(self, text="Low")
        self.lowestLabel.grid(column=6, row=1)
        self._lowestValueVar = tk.DoubleVar()
        self.lowestValue = tk.Label(self, text="0.000", textvariable=self._lowestValueVar)
        self.lowestValue.grid(column=7, row=1)

        # VWAP
        self.vwapLabel = tk.Label(self, text="VWAP")
        self.vwapLabel.grid(column=8, row=1)
        self._vwapValueVar = tk.DoubleVar()
        self.vwapValue = tk.Label(self, text="0.000", textvariable=self._vwapValueVar)
        self.vwapValue.grid(column=9, row=1)

        # L1 Bid
        self.bidLabel = tk.Label(self, text="Bid")
        self.bidLabel.grid(column=0, row=2)
        self._bidValueVar = tk.DoubleVar()
        self.bidValue = tk.Label(self, text="0.000", textvariable=self._bidValueVar)
        self.bidValue.grid(column=1, row=2)

        # L1 Bid Size
        self.bidSizeLabel = tk.Label(self, text="Bid Size")
        self.bidSizeLabel.grid(column=2, row=2)
        self._bidSizeValueVar = tk.DoubleVar()
        self.bidSizeValue = tk.Label(self, text="0", textvariable=self._bidSizeValueVar)
        self.bidSizeValue.grid(column=3, row=2)

        # L1 Ask
        self.askLabel = tk.Label(self, text="Ask")
        self.askLabel.grid(column=4, row=2)
        self._askValueVar = tk.DoubleVar()
        self.askValue = tk.Label(self, text="0", textvariable=self._askValueVar)
        self.askValue.grid(column=5, row=2)

        # L1 Ask Size
        self.askSizeLabel = tk.Label(self, text="Ask Size")
        self.askSizeLabel.grid(column=6, row=2)
        self._askSizeValueVar = tk.DoubleVar()
        self.askSizeValue = tk.Label(self, text="0", textvariable=self._askSizeValueVar)
        self.askSizeValue.grid(column=7, row=2)

        # Exchange
        self.exchangeLabel = tk.Label(self, text="Exchange")
        self.exchangeLabel.grid(column=8, row=2)
        self._exchangeValueVar = tk.StringVar()
        self.exchangeValue = tk.Label(self, text="", textvariable=self._exchangeValueVar)
        self.exchangeValue.grid(column=9, row=2)

        depthColumns = ("Price", "Volume")
        # L2 Bid
        self.bidTree = ttk.Treeview(self, columns=depthColumns, show="headings")
        self.bidTree.grid(column=0, row=3, columnspan=3)
        self.bidTree.column("Price", width=140)
        self.bidTree.heading("Price", text="Price")
        self.bidTree.column("Volume", width=70)
        self.bidTree.heading("Volume", text="Volume")

        # L2 Ask
        self.askTree = ttk.Treeview(self, columns=depthColumns, show="headings")
        self.askTree.grid(column=3, row=3, columnspan=3)
        self.askTree.column("Price", width=140)
        self.askTree.heading("Price", text="Price")
        self.askTree.column("Volume", width=70)
        self.askTree.heading("Volume", text="Volume")

        # Tape
        self.tapeTree = ttk.Treeview(self, columns=depthColumns, show="headings")
        self.tapeTree.grid(column=6, row=3, columnspan=3)
        self.tapeTree.column("Price", width=140)
        self.tapeTree.heading("Price", text="Price")
        self.tapeTree.column("Volume", width=70)
        self.tapeTree.heading("Volume", text="Volume")
        self.tapeTree.tag_configure("buy", background="green")
        self.tapeTree.tag_configure("sell", background="red")

        # Order Quantity
        self.orderQuantityLabel = tk.Label(self, text="Quantity")
        self.orderQuantityLabel.grid(column=0, row=4, columnspan=3)
        self._orderQuantityValueVar = tk.DoubleVar()
        self.orderQuantityValue = tk.Spinbox(self, from_=1, to=99999999, textvariable=self._orderQuantityValueVar)
        self.orderQuantityValue.grid(column=0, row=5, columnspan=3)

        # Order Type
        self.orderTypeLabel = tk.Label(self, text="Type")
        self.orderTypeLabel.grid(column=3, row=4, columnspan=2)
        orderTypes = ("LIMIT", "MARKET", "QUOTE")
        self._orderTypeValueVar = tk.StringVar()
        self.orderTypeValue = ttk.Combobox(self, values=orderTypes, textvariable=self._orderTypeValueVar)
        self.orderTypeValue.grid(column=3, row=5, columnspan=2)

        # Order Route
        self.orderRouteLabel = tk.Label(self, text="Route")
        self.orderRouteLabel.grid(column=5, row=4, columnspan=2)
        self.orderRouteValue = ttk.Combobox(self)
        self.orderRouteValue.grid(column=5, row=5, columnspan=2)

        # Order Expiration
        self.orderExpirationLabel = tk.Label(self, text="Expiration")
        self.orderExpirationLabel.grid(column=7, row=4, columnspan=2)
        expirationTypes=("Good For Day", "Good Until Cancelled")
        self._orderExpirationValueVar = tk.StringVar()
        self.orderExpirationValue = ttk.Combobox(self, values=expirationTypes, textvariable=self._orderExpirationValueVar)
        self.orderExpirationValue.grid(column=7, row=5, columnspan=2)

        # Price
        self.priceLabel = tk.Label(self, text="Price")
        self.priceLabel.grid(column=0, row=6, columnspan=3)
        self._priceValueVar = tk.DoubleVar()
        self.priceValue = tk.Spinbox(self, from_=0, to=999999999, textvariable=self._priceValueVar)
        self.priceValue.grid(column=0, row=7, columnspan=3)

        # Stop Loss
        self.stopLossLabel = tk.Label(self, text="Stop")
        self.stopLossLabel.grid(column=3, row=6, columnspan=2)
        self._stopLossValueVar = tk.DoubleVar()
        self.stopLossValue = tk.Spinbox(self, from_=0, to=99999999, textvariable=self._stopLossValueVar)
        self.stopLossValue.grid(column=3, row=7, columnspan=2)

        # Take Profit
        self.takeProfitLabel = tk.Label(self, text="Take")
        self.takeProfitLabel.grid(column=5, row=6, columnspan=2)
        self._takeProfitValueVar = tk.DoubleVar()
        self.takeProfitValue = tk.Spinbox(self, from_=0, to=99999999, textvariable=self._takeProfitValueVar)
        self.takeProfitValue.grid(column=5, row=7, columnspan=2)

        # Entry Type
        self.entryTypeLabel = tk.Label(self, text="Entry Type")
        self.entryTypeLabel.grid(column=7, row=6, columnspan=2)
        entryTypes = ("Deal", "Working Order")
        self._entryTypeValueVar = tk.StringVar()
        self.entryTypeValue = ttk.Combobox(self, values=entryTypes, textvariable=self._entryTypeValueVar)
        self.entryTypeValue.grid(column=7, row=7, columnspan=2)

        # Buy Button
        self.buyButton = tk.Button(self, text="Buy 0.00", command=self.longEntry)
        self.buyButton.grid(column=0, row=9, columnspan=3)

        # Sell Button
        self.sellButton = tk.Button(self, text="Sell 0.00", command=self.longClose)
        self.sellButton.grid(column=3, row=9, columnspan=2)

        # Short Button
        self.shortButton = tk.Button(self, text="Short 0.00", command=self.shortEntry)
        self.shortButton.grid(column=5, row=9, columnspan=2)

        # Cover Button
        self.coverButton = tk.Button(self, text="Cover 0.00", command=self.shortClose)
        self.coverButton.grid(column=7, row=9, columnspan=2)

        self.pack()

    def _onClose(self):
        if self._subscription_token != None:
            self.broker.unsubscribeSymbols(self._subscription_token)

        self.parent.destroy()

    def longEntry(self):
        if self.broker != None:
            entryType = self._entryTypeValueVar.get()
            if entryType != "":
                if entryType == "Deal":
                    self.broker.dealEntry(False, self._currentSymbol, self._priceValueVar.get(), self._orderQuantityValueVar.get(), "LONG", self._orderTypeValueVar.get(), self._stopLossValueVar.get(), self._takeProfitValueVar.get())
                elif entryType == "Working Order":
                    self.broker.dealWorkingOrder(False, self._currentSymbol, self._priceValueVar.get(), self._orderQuantityValueVar.get(), "LONG", self._orderTypeValueVar.get(), self._stopLossValueVar.get(), self._takeProfitValueVar.get(), self._orderExpirationValueVar.get())

    def longClose(self):
        if self.broker != None:
            entryType = self._entryTypeValueVar.get()
            if entryType != "":
                if entryType == "Deal":
                    self.broker.closeEntry(False, self._currentSymbol, self._priceValueVar.get(), self._orderQuantityValueVar.get(), "SELL", self._orderTypeValueVar.get(), self._stopLossValueVar.get(), self._takeProfitValueVar.get())
                elif entryType == "Working Order":
                    self.broker.dealWorkingOrder(False, self._currentSymbol, self._priceValueVar.get(), self._orderQuantityValueVar.get(), "SELL", self._orderTypeValueVar.get(), self._stopLossValueVar.get(), self._takeProfitValueVar.get(), self._orderExpirationValueVar.get())

    def shortEntry(self):
        if self.broker != None:
            entryType = self._entryTypeValueVar.get()
            if entryType != "":
                if entryType == "Deal":
                    self.broker.dealEntry(False, self._currentSymbol, self._priceValueVar.get(), self._orderQuantityValueVar.get(), "SHORT", self._orderTypeValueVar.get(), self._stopLossValueVar.get(), self._takeProfitValueVar.get())
                elif entryType == "Working Order":
                    self.broker.dealWorkingOrder(False, self._currentSymbol, self._priceValueVar.get(), self._orderQuantityValueVar.get(), "SHORT", self._orderTypeValueVar.get(), self._stopLossValueVar.get(), self._takeProfitValueVar.get(), self._orderExpirationValueVar.get())

    def shortClose(self):
        if self.broker != None:
            entryType = self._entryTypeValueVar.get()
            if entryType != "":
                if entryType == "Deal":
                    self.broker.closeEntry(False, self._currentSymbol, self._priceValueVar.get(), self._orderQuantityValueVar.get(), "BUY", self._orderTypeValueVar.get(), self._stopLossValueVar.get(), self._takeProfitValueVar.get())
                elif entryType == "Working Order":
                    self.broker.dealWorkingOrder(False, self._currentSymbol, self._priceValueVar.get(), self._orderQuantityValueVar.get(), "BUY", self._orderTypeValueVar.get(), self._stopLossValueVar.get(), self._takeProfitValueVar.get(), self._orderExpirationValueVar.get())

    def symbolTextChanged(self, *args):
        symbol = self._symbolVar.get()
        # Search history maybe?

    def getInstrument(self, event=None):
        if self.broker != None:
            wantedSymbol = self._symbolVar.get()
            if wantedSymbol in self.kekka_map:
                self.setSubscribedInstrument()
                return

            result = self.broker.findInstrument(self._symbolVar.get())
            marketList = []
            self.kekka_map.clear()
            for market in result:
                marketList.append(market.name)
                self.kekka_map[market.name] = market.apiName

            self.symbolPicker['values'] = marketList
            self.symbolPicker.event_generate('<1>')

    def setSubscribedInstrument(self, *args):
        if self.broker != None:
            instrument = self.broker.getInstrument(self.kekka_map[self._symbolVar.get()])
            self._currentSymbol=instrument
            self._bidValueVar.set(instrument.bid)
            self._askValueVar.set(instrument.ask)
            self._highestValueVar.set(instrument.high)
            self._lowestValueVar.set(instrument.low)
            self._changeLabelVar.set(instrument.netChange)
            self._changePercentVar.set("%f%%" % (instrument.percentChange))
            self._openValueVar.set(instrument.open)
            self._closeValueVar.set(instrument.close)
            self._bidSizeValueVar.set(instrument.bidSize)
            self._askSizeValueVar.set(instrument.askSize)
            self._vwapValueVar.set(instrument.vwap)
            self._lastVolumeLabelVar.set(instrument.lastVolume)
            self._exchangeValueVar.set(instrument.exchange)
            self._nextRefreshValueVar.set(instrument.nextRefresh)

            self.bidTree.delete(*self.bidTree.get_children())
            for bid in instrument.bidDepth:
                self.bidTree.insert('', 'end', values=(bid[0], bid[1]))

            self.askTree.delete(*self.askTree.get_children())
            for ask in instrument.askDepth:
                self.askTree.insert('', 'end', values=(ask[0], ask[1]))

            self.tapeTree.delete(*self.tapeTree.get_children())
            for tape in instrument.tapeDepth:
                self.tapeTree.insert('', 'end', values=(tape[0], tape[1]), tags=("buy" if tape[3]=="b" else "sell",))

            if self._subscription_token != None:
                self.broker.unsubscribeSymbols(self._subscription_token)

            self._subscription_token = self.broker.subscribeSymbols([self.kekka_map[self._symbolVar.get()]], ["BID", "OFFER", "HIGH", "LOW", "MID_OPEN", "CHANGE"], self.tickerEvent)

            self.broker.getInstrumentPrices(self.kekka_map[self._symbolVar.get()])

    def tickerEvent(self, data):
        self._openValueVar.set(data.open)
        self._highestValueVar.set(data.high)
        self._lowestValueVar.set(data.low)
        self._closeValueVar.set(data.close)
        self._vwapValueVar.set(data.vwap)
        self._bidValueVar.set(data.bid)
        self._bidSizeValueVar.set(data.bidSize)
        self._askValueVar.set(data.ask)
        self._askSizeValueVar.set(data.askSize)
        self._lastVolumeLabelVar.set(data.lastVolume)
        self._nextRefreshValueVar.set(data.nextRefresh)

        self.bidTree.delete(*self.bidTree.get_children())
        for bid in data.bidDepth:
            self.bidTree.insert('', 'end', values=(bid[0], bid[1]))

        self.askTree.delete(*self.askTree.get_children())
        for ask in data.askDepth:
            self.askTree.insert('', 'end', values=(ask[0], ask[1]))

        self.tapeTree.delete(*self.tapeTree.get_children())
        for tape in data.tapeDepth:
            self.tapeTree.insert('', 'end', values=(tape[0], tape[1]), tags=("buy" if tape[3]=="b" else "sell",))
            