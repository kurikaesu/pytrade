import tkinter as tk
import tkinter.ttk as ttk

class Settings(tk.Frame):
    def __init__(self, parent=None, application=None, pluginList=None):
        super(Settings, self).__init__(parent)
        self.app = application
        self.pluginList = pluginList

        self.brokerLabel = tk.Label(self, text="Broker")
        self.brokerLabel.grid(column=0, row=0)

        comboValues = []
        for name, plugin in self.pluginList.items():
            comboValues.append(name)

        self.brokerCombo = ttk.Combobox(self, values=comboValues)
        self.brokerCombo.grid(column=1, row=0)

        self.brokerSettingsButton = tk.Button(self, text="Configure", command=self.configureBroker)
        self.brokerSettingsButton.grid(column=2, row=0)

        self.pack()

    def configureBroker(self):
        brokerName = self.brokerCombo.get()
        if brokerName in self.pluginList:
            self.pluginList[brokerName].showConfig(tk.Toplevel(self.master))
