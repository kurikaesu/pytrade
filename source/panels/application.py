import tkinter as tk
import tkinter.ttk as ttk

from .chart import *
from .depth_tape import *

class Application(tk.Frame):
    def __init__(self, parent=None):
        super(Application, self).__init__(parent)
        self.master.title("PyTrade")

        self.openChartButton = tk.Button(self, text="New Chart Window", command=self.openChart)
        self.openChartButton.pack()
        self.openOrderButton = tk.Button(self, text="Open Order Panel", command=self.openOrderPanel)
        self.openOrderButton.pack()
        self.pack()

    def openChart(self):
        rootWindow = tk.Toplevel(self.master)
        chart = Chart(rootWindow)

    def openOrderPanel(self):
        rootWindow = tk.Toplevel(self.master)
        orderPanel = DepthTape(rootWindow)
