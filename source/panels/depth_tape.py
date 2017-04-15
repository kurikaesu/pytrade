import tkinter as tk
import tkinter.ttk as ttk

import json

class DepthTape(tk.Frame):
    def __init__(self, parent=None, broker=None):
        super(DepthTape, self).__init__(parent)
        self.broker = broker
        self.kekka_map = {}
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
        self.lastVolumeLabel = tk.Label(self, text="0")
        self.lastVolumeLabel.grid(column=7, row=0)

        # L1 Open
        self.openLabel = tk.Label(self, text="Open")
        self.openLabel.grid(column=0, row=1)
        self.openValue = tk.Label(self, text="0.000")
        self.openValue.grid(column=1, row=1)

        # L1 Close
        self.closeLabel = tk.Label(self, text="Close")
        self.closeLabel.grid(column=2, row=1)
        self.closeValue = tk.Label(self, text="0.000")
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
        self.vwapValue = tk.Label(self, text="0.000")
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
        self.bidSizeValue = tk.Label(self, text="0")
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
        self.askSizeValue = tk.Label(self, text="0")
        self.askSizeValue.grid(column=7, row=2)

        # Exchange
        self.exchangeLabel = tk.Label(self, text="Exchange")
        self.exchangeLabel.grid(column=8, row=2)
        self.exchangeValue = tk.Label(self, text="")
        self.exchangeValue.grid(column=9, row=2)

        # L2 Bid

        # L2 Ask

        # Tape

        # Order Quantity
        self.orderQuantityLabel = tk.Label(self, text="Quantity")
        self.orderQuantityLabel.grid(column=0, row=4, columnspan=3)
        self.orderQuantityValue = tk.Spinbox(self, from_=1, to=99999999)
        self.orderQuantityValue.grid(column=0, row=5, columnspan=3)

        # Order Type
        self.orderTypeLabel = tk.Label(self, text="Type")
        self.orderTypeLabel.grid(column=3, row=4, columnspan=2)
        self.orderTypeValue = ttk.Combobox(self)
        self.orderTypeValue.grid(column=3, row=5, columnspan=2)

        # Order Route
        self.orderRouteLabel = tk.Label(self, text="Route")
        self.orderRouteLabel.grid(column=5, row=4, columnspan=2)
        self.orderRouteValue = ttk.Combobox(self)
        self.orderRouteValue.grid(column=5, row=5, columnspan=2)

        # Order Expiration
        self.orderExpirationLabel = tk.Label(self, text="Expiration")
        self.orderExpirationLabel.grid(column=7, row=4, columnspan=2)
        self.orderExpirationValue = ttk.Combobox(self)
        self.orderExpirationValue.grid(column=7, row=5, columnspan=2)

        # Price
        self.priceLabel = tk.Label(self, text="Price")
        self.priceLabel.grid(column=0, row=6, columnspan=3)
        self.priceValue = tk.Spinbox(self, from_=0, to=999999999)
        self.priceValue.grid(column=0, row=7, columnspan=3)

        # Buy Button
        self.buyButton = tk.Button(self, text="Buy 0.00")
        self.buyButton.grid(column=0, row=9, columnspan=3)

        # Sell Button
        self.sellButton = tk.Button(self, text="Sell 0.00")
        self.sellButton.grid(column=3, row=9, columnspan=2)

        # Short Button
        self.shortButton = tk.Button(self, text="Short 0.00")
        self.shortButton.grid(column=5, row=9, columnspan=2)

        # Cover Button
        self.coverButton = tk.Button(self, text="Cover 0.00")
        self.coverButton.grid(column=7, row=9, columnspan=2)

        self.pack()

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
            self._bidValueVar.set(instrument.bid)
            self._askValueVar.set(instrument.ask)
            self._highestValueVar.set(instrument.high)
            self._lowestValueVar.set(instrument.low)
            self._changeLabelVar.set(instrument.netChange)
            self._changePercentVar.set("%f%%" % (instrument.percentChange))
            