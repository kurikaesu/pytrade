import tkinter as tk
import tkinter.ttk as ttk

import datetime
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class Candle:
    def __init__(self):
        self._timestamp = None
        self._open = None
        self._high = None
        self._low = None
        self._close = None

    def timestamp(self):
        return self._timestamp

    def setTimestamp(self, newTimestamp=None):
        self._timestamp = newTimestamp

    def open(self):
        return self._open

    def setOpen(self, newOpen=None):
        self._open = newOpen

    def high(self):
        return self._high

    def setHigh(self, newHigh=None):
        self._high = newHigh

    def low(self):
        return self._low

    def setLow(self, newLow=None):
        self._low = newLow

    def close(self):
        return self._close

    def setClose(self, newClose=None):
        self._close = newClose

    def lastPrint(self, lastPrint=None):
        if lastPrint == None:
            raise ValueError("The last print value cannot be None")

        if self._close == None:
            self._open = self._high = self._low = self._close = lastPrint
            return

        self._close = lastPrint

        if lastPrint > self._high:
            self._high = lastPrint

        if lastPrint < self._low:
            self._low = lastPrint


class Chart(tk.Frame):
    def __init__(self, parent=None):
        super(Chart, self).__init__(parent)
        self._candles = []
        self._candleGroupSize = 1
        self._aggregateCandles = []

        startDelta = datetime.timedelta(days=datetime.date.today().weekday(), weeks=1)
        self._endTimestamp = datetime.date.today()
        self._startingTimestamp = self._endTimestamp - startDelta

        self._symbolLabel = tk.Label(self, text="Instrument")
        self._symbolLabel.grid(column=0, row=0)
        self._symbolComboboxVal = tk.StringVar()
        self._symbolCombobox = ttk.Combobox(self, textvariable=self._symbolComboboxVal)
        self._symbolCombobox.bind('<Return>', self._setInstrument)
        self._symbolCombobox.grid(column=1, row=0)

        self._instrument = None
        self._figure = Figure(figsize=(15, 4), dpi=100)
        self._axes = self._figure.add_subplot(111)

        self._canvas = FigureCanvasTkAgg(self._figure, self)
        self._canvas.show()
        self._canvas.get_tk_widget().grid(column=0, row=1, columnspan=4)


        self.button = tk.Button(self, text="Redraw", command=self.redraw)
        self.button.grid(column=0, row=2)

        self.pack()

    def _setInstrument(self, *args):
        self._instrument = self._symbolComboboxVal.get()
        self.redraw()

    def setInstrumentName(self, instrumentName):
        self._instrument = instrumentName

    def setGroupSize(self, newGroupSize=1):
        self._candleGroupSize = newGroupSize

    def setStartTimestamp(self, timeStamp):
        self._startingTimestamp = timeStamp

    def setEndTimestamp(self, timeStamp):
        self._endTimestamp = timeStamp

    def processPrint(self, lastPrint=None):
        if lastPrint == None:
            pass #This should throw an exception

    def redraw(self):
        self._axes.clear()
        if self._instrument != None:
            try:
                fh = finance.quotes_historical_yahoo_ohlc(self._instrument, self._startingTimestamp, self._endTimestamp)
                prices = fh
                finance.candlestick_ohlc(self._axes, prices, width=0.6)
                self._canvas.draw()
            except Exception:
                print("Couldn't find symbol")
