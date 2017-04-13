import tkinter as tk
import tkinter.ttk as ttk

from .settings import *
from .chart import *
from .depth_tape import *
from .journal import *

class Application(tk.Frame):
    def __init__(self, parent=None, crypto=None, database=None):
        super(Application, self).__init__(parent)
        self.master.title("PyTrade")
        self._crypto = crypto
        self._db = database

        self.openChartButton = tk.Button(self, text="New Chart Window", command=self.openChart)
        self.openChartButton.pack()
        self.openOrderButton = tk.Button(self, text="Open Order Panel", command=self.openOrderPanel)
        self.openOrderButton.pack()
        self.journalButton = tk.Button(self, text="Trading Journal", command=self.openTradingJournal)
        self.journalButton.pack()
        self.settingsButton = tk.Button(self, text="Settings", command=self.openSettingsWindow)
        self.settingsButton.pack()
        self.pack()

        self.brokerPlugins = None
        self.currentBroker = None

    def setBrokerPlugins(self, plugins):
        self.brokerPlugins = plugins

    def setCurrentBroker(self, broker):
        self.currentBroker = self.brokerPlugins[broker]

    def openChart(self):
        rootWindow = tk.Toplevel(self.master)
        chart = Chart(rootWindow)

    def openOrderPanel(self):
        rootWindow = tk.Toplevel(self.master)
        orderPanel = DepthTape(rootWindow)

    def openTradingJournal(self):
        rootWindow = tk.Toplevel(self.master)
        tradingJournal = Journal(rootWindow, self._db, self._crypto)

    def openSettingsWindow(self):
        rootWindow = tk.Toplevel(self.master)
        settingsWindow = Settings(rootWindow, self, self.brokerPlugins)
