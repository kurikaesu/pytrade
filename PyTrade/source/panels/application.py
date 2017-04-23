from tkinter import *
from .settings import *
from .chart import *
from .depth_tape import *
from .journal import *

class Application(tk.Frame):

    def __init__(self, parent=None, crypto=None, database=None, vc=None):
        super(Application, self).__init__(parent)
        self.master.title("PyTrade")
        self._crypto = crypto
        self._db = database



        self.brokerPlugins = None
        self.currentBroker = None
        self.__init_layout()

        self.loadSettings()

    def __init_layout(self):

        name_label = tk.Label(self, text='Username: ')
        name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self, )
        self.name_entry.grid(row=0, column=1)

        pwd_label = tk.Label(self, text='Password: ')
        pwd_label.grid(row=0, column=2)
        self.pwd_entry = tk.Entry(self, show='*')
        self.pwd_entry.grid(row=0, column=3)

        self.sign_up_button = tk.Button(self, text='Sign Up')
        self.sign_up_button.grid(row=0, column=5)
        self.sign_up_button.config(state=DISABLED)

        self.sign_in_button = tk.Button(self, text='Sign In')
        self.sign_in_button.grid(row=0, column=6)
        self.sign_in_button.config(state=DISABLED)
        self.pwd_entry.bind('<Key>', self.__pwd_entry_callback)
        self.openChartButton = tk.Button(self, text="New Chart Window", command=self.openChart)
        self.openChartButton.grid(row=1, column=0)
        self.openOrderButton = tk.Button(self, text="Open Order Panel", command=self.openOrderPanel)
        self.openOrderButton.grid(row=1, column=1)
        self.journalButton = tk.Button(self, text="Trading Journal", command=self.openTradingJournal)
        self.journalButton.grid(row=1, column=2)
        self.settingsButton = tk.Button(self, text="Settings", command=self.openSettingsWindow)
        self.settingsButton.grid(row=1, column=3)
        self.pack()


    def loadSettings(self):
        pass

    def setBrokerPlugins(self, plugins):
        self.brokerPlugins = plugins

    def setCurrentBroker(self, broker):
        print("Setting broker to %s" % (broker))
        self.currentBroker = self.brokerPlugins[broker]

    def openChart(self):
        rootWindow = tk.Toplevel(self.master)
        chart = Chart(rootWindow)

    def openOrderPanel(self):
        rootWindow = tk.Toplevel(self.master)
        orderPanel = DepthTape(rootWindow, self.currentBroker)

    def openTradingJournal(self):
        rootWindow = tk.Toplevel(self.master)
        tradingJournal = Journal(rootWindow, self._db, self._crypto)

    def openSettingsWindow(self):
        print("te")
        rootWindow = tk.Toplevel(self.master)
        settingsWindow = Settings(rootWindow, self, self.brokerPlugins)

    def get_username(self):
        return self.name_entry.get()

    def get_password(self):
        return self.pwd_entry.get()

    def __pwd_entry_callback(self, event = None):
        if (len(self.get_username()) > 0) & (len(self.get_password()) > 0):
            self.__enable_sign_in_btn(True)
            self.__enable_sign_up_btn(True)
        else:
            self.__enable_sign_in_btn(False)
            self.__enable_sign_up_btn(False)
        pass


    def __enable_sign_in_btn(self, bool):
        if bool:
            print("Sign in enabled")
            self.sign_in_button.config(state=NORMAL)
        else:
            self.sign_in_button.config(state=DISABLED)

    def __enable_sign_up_btn(self, bool):
        if bool:
            self.sign_up_button.config(state=NORMAL)
        else:
            self.sign_up_button.config(state=DISABLED)
