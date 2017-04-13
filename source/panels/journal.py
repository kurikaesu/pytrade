import tkinter as tk
import tkinter.ttk as ttk

import json
import sqlite3

class JournalEntry:
    def __init__(self, parentJournal = None, myId=None):
        self._parentJournal = parentJournal

        self._id = myId
        self.data = {}
        self.data['timestamp'] = None
        self.data['market'] = None
        self.data['instrument'] = None
        self.data['setup'] = None
        self.data['entryprice'] = None
        self.data['entrysize'] = None
        self.data['stoploss'] = None
        self.data['takeprofit'] = None
        self.data['closeprice'] = None
        self.data['profitloss'] = None
        self.data['fees'] = None

    def setId(self, myId):
        self._id = myId

    def getId(self):
        return self._id

    def setParentJournal(self, parentJournal = None):
        self._parentJournal = parentJournal

    def setTimestamp(self, timestamp):
        self.data['timestamp'] = timestamp

    def setMarket(self, market):
        self.data['market'] = market

    def setInstrument(self, instrument):
        self.data['instrument'] = instrument

    def setSetup(self, setup):
        self.data['setup'] = setup

    def setEntryPrice(self, entryPrice):
        self.data['entryprice'] = entryPrice

    def setEntrySize(self, entrySize):
        self.data['entrysize'] = entrySize

    def setStopLoss(self, stopLoss):
        self.data['stoploss'] = stopLoss

    def setTakeProfit(self, takeProfit):
        self.data['takeprofit'] = takeProfit

    def setClosePrice(self, closePrice):
        self.data['closeprice'] = closePrice

    def setProfitLoss(self, profitLoss):
        self.data['profitloss'] = profitLoss

    def setFees(self, fees):
        self.data['fees'] = fees

    def Save(self):
        if self._parentJournal != None:
            self._parentJournal.addEntry(self)
        else:
            raise RuntimeError("Parent journal for this entry not set")

    def asListRow(self):
        return (self._id, self.data['timestamp'], self.data['market'], self.data['instrument'],
            self.data['setup'], self.data['entryprice'], self.data['entrysize'],
            self.data['stoploss'], self.data['takeprofit'], self.data['closeprice'],
            self.data['profitloss'], self.data['fees'])

    def toJson(self):
        return json.dumps(self.data)

    def fromJson(self, jsonString):
        self.data = json.loads(jsonString)

class JournalEntryEditor(tk.Frame):
    def __init__(self, parent, journal, data=None):
        super(JournalEntryEditor, self).__init__(parent)
        self._entry = journal.newEntry()

        self._entryDateLabel = tk.Label(self, text="Entry Date")
        self._entryDateLabel.grid(column=0, row=0)

        self._marketVar = tk.StringVar()
        self._marketLabel = tk.Label(self, text="Market")
        self._marketLabel.grid(column=0, row=2)
        self._marketValue = ttk.Combobox(self, textvariable=self._marketVar)
        self._marketValue.grid(column=0, row=3)

        self._instrumentVar = tk.StringVar()
        self._instrumentLabel = tk.Label(self, text="Instrument")
        self._instrumentLabel.grid(column=0, row=4)
        self._instrumentValue = ttk.Combobox(self, textvariable=self._instrumentVar)
        self._instrumentValue.grid(column=0, row=5)

        self._setupVar = tk.StringVar()
        self._setupLabel = tk.Label(self, text="Setup")
        self._setupLabel.grid(column=0, row=6)
        self._setupValue = ttk.Combobox(self, textvariable=self._setupVar)
        self._setupValue.grid(column=0, row=7)

        self._entryPriceVar = tk.DoubleVar(0)
        self._entryPriceLabel = tk.Label(self, text="Entry Price")
        self._entryPriceLabel.grid(column=1, row=0)
        self._entryPriceValue = tk.Entry(self, textvariable=self._entryPriceVar)
        self._entryPriceValue.grid(column=1, row=1)

        self._entrySizeVar = tk.DoubleVar(0)
        self._entrySizeLabel = tk.Label(self, text="Size")
        self._entrySizeLabel.grid(column=1, row=2)
        self._entrySizeValue = tk.Entry(self, textvariable=self._entrySizeVar)
        self._entrySizeValue.grid(column=1, row=3)

        self._stopLossVar = tk.DoubleVar(0)
        self._stopLossLabel = tk.Label(self, text="Stop Loss")
        self._stopLossLabel.grid(column=1, row=4)
        self._stopLossValue = tk.Entry(self, textvariable=self._stopLossVar)
        self._stopLossValue.grid(column=1, row=5)

        self._closeDateLabel = tk.Label(self, text="Close Date")
        self._closeDateLabel.grid(column=2, row=0)

        self._closePriceVar = tk.DoubleVar(0)
        self._closePriceLabel = tk.Label(self, text="Close Price")
        self._closePriceLabel.grid(column=2, row=2)
        self._closePriceValue = tk.Entry(self, textvariable=self._closePriceVar)
        self._closePriceValue.grid(column=2, row=3)

        self._profitLossVar = tk.DoubleVar(0)
        self._profitLossLabel = tk.Label(self, text="Profit/Loss")
        self._profitLossLabel.grid(column=2, row=4)
        self._profitLossValue = tk.Entry(self, textvariable=self._profitLossVar)
        self._profitLossValue.grid(column=2, row=5)

        self._feesVar = tk.DoubleVar(0)
        self._feesLabel = tk.Label(self, text="Fees")
        self._feesLabel.grid(column=2, row=6)
        self._feesValue = tk.Entry(self, textvariable=self._feesVar)
        self._feesValue.grid(column=2, row=7)

        self._saveButton = tk.Button(self, text="Save", command=self.save)
        self._saveButton.grid(column=0, row=10)

        self.pack()

    def save(self):
        self._entry.setMarket(self._marketVar.get())
        self._entry.setInstrument(self._instrumentVar.get())
        self._entry.setSetup(self._setupVar.get())
        self._entry.setEntryPrice(self._entryPriceVar.get())
        self._entry.setEntrySize(self._entrySizeVar.get())
        self._entry.setStopLoss(self._stopLossVar.get())
        self._entry.setClosePrice(self._closePriceVar.get())
        self._entry.setProfitLoss(self._profitLossVar.get())
        self._entry.setFees(self._feesVar.get())

        self._entry.Save()

class Journal(tk.Frame):
    def __init__(self, parent, db, crypt):
        super(Journal, self).__init__(parent)
        self._entries = []
        self._db = db
        self._cursor = self._db.cursor()
        self._crypt = crypt

        self._insertStatement = "INSERT INTO journal_entries(data) VALUES (?)"
        self._deleteStatement = "DELETE FROM journal_entries WHERE id=?"

        self._tradeListLabel = tk.Label(self, text="Trading Data")
        self._tradeListLabel.grid(column=0, row=0 )

        journalColumns = ("#", "Entry Date", "Market", "Instrument", "Setup", "Position", "Size", "Entry", "Exit", "P/L", "Fees")

        self._journalList = ttk.Treeview(self, columns=journalColumns, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self._journalList.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self._journalList.xview)
        self._journalList.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self._journalList.grid(column=0, row=1)

        self._addEntryButton = tk.Button(self, text="Add Entry", command=self.createNewEntry)
        self._addEntryButton.grid(column=0, row=2)

        self.loadEntries()

        self.pack()

    def loadEntries(self):
        try:
            for row in self._cursor.execute("SELECT id, data FROM journal_entries ORDER BY id ASC"):
                entry = JournalEntry(self, row[0])
                entry.fromJson(self._crypt.decryptBytes(row[1]))
                self._entries.append(entry)
                self._journalList.insert('', 'end', values=entry.asListRow())
        except sqlite3.OperationalError:
            self._cursor.execute("CREATE TABLE journal_entries (id INTEGER PRIMARY KEY, data TEXT)")
            self._db.commit()

    def newEntry(self):
        return JournalEntry(self)

    def addEntry(self, jEntry):
        self._cursor.execute(self._insertStatement, (self._crypt.encryptBytes(jEntry.toJson().encode()),) )
        self._db.commit()
        jEntry.setId(self._cursor.lastrowid)
        self._entries.append(jEntry)
        self._journalList.insert('', 'end', values=jEntry.asListRow())

    def deleteEntry(self, jEntry):
        self._entries.remove(jEntry)
        self._cursor.execute(self._deleteStatement, (jEntry.getId(),))
        self._db.commit()

    def getEntry(self):
        pass

    def updateEntry(self):
        pass

    def createNewEntry(self):
        rootWindow = tk.Toplevel(self.master)
        newEntryWindow = JournalEntryEditor(rootWindow, self)
