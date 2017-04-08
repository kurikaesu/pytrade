import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Frame):
    def __init__(self, parent=None):
        super(Application, self).__init__(parent)
        self.master.title("PyTrade")
