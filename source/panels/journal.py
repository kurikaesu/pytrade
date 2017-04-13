import tkinter as tk
import tkinter.ttk as ttk

import json
import sqlite3

class JournalEntry:
    def __init__(self, parentJournal = None, myId=None):
        self._parentJournal = parentJournal

        self._id = myId
        self._timestamp = None
        self._market = None
        self._instrument = None
        self._setup = None
        self._entryprice = None
        self._entrysize = None
        self._stoploss = None
        self._takeprofit = None
        self._closeprice = None
        self._profitloss = None
        self._fees = None

    def setId(self, myId):
        self._id = myId

    def getId(self):
        return self._id

    def setParentJournal(self, parentJournal = None):
        self._parentJournal = parentJournal

    def setTimestamp(self, timestamp):
        self._timestamp = timestamp

    def setMarket(self, market):
        self._market = market

    def Save(self):
        if self._parentJournal != None:
            self._parentJournal.addEntry(self)
        else:
            raise RuntimeError("Parent journal for this entry not set")

    def toJson(self):
        pass

    def fromJson(self, jsonString):
        pass

class JournalEntryEditor(tk.Frame):
    def __init__(self, parent, journal, data=None):
        super(JournalEntryEditor, self).__init__(parent)
        self._entry = journal.newEntry()

        self._entryDateLabel = tk.Label(self, text="Entry Date")
        self._entryDateLabel.grid(column=0, row=0)

        self._marketLabel = tk.Label(self, text="Market")
        self._marketLabel.grid(column=0, row=2)
        self._marketValue = ttk.Combobox(self)
        self._marketValue.grid(column=0, row=3)

        self._instrumentLabel = tk.Label(self, text="Instrument")
        self._instrumentLabel.grid(column=0, row=4)
        self._instrumentValue = ttk.Combobox(self)
        self._instrumentValue.grid(column=0, row=5)

        self._setupLabel = tk.Label(self, text="Setup")
        self._setupLabel.grid(column=0, row=6)
        self._setupValue = ttk.Combobox(self)
        self._setupValue.grid(column=0, row=7)

        self._entryPriceLabel = tk.Label(self, text="Entry Price")
        self._entryPriceLabel.grid(column=1, row=0)
        self._entryPriceValue = tk.Entry(self)
        self._entryPriceValue.grid(column=1, row=1)

        self._entrySizeLabel = tk.Label(self, text="Size")
        self._entrySizeLabel.grid(column=1, row=2)
        self._entrySizeValue = tk.Entry(self)
        self._entrySizeValue.grid(column=1, row=3)

        self._stopLossLabel = tk.Label(self, text="Stop Loss")
        self._stopLossLabel.grid(column=1, row=4)
        self._stopLossValue = tk.Entry(self)
        self._stopLossValue.grid(column=1, row=5)

        self._closeDateLabel = tk.Label(self, text="Close Date")
        self._closeDateLabel.grid(column=2, row=0)

        self._closePriceLabel = tk.Label(self, text="Close Price")
        self._closePriceLabel.grid(column=2, row=2)
        self._closePriceValue = tk.Entry(self)
        self._closePriceValue.grid(column=2, row=3)

        self._profitLossLabel = tk.Label(self, text="Profit/Loss")
        self._profitLossLabel.grid(column=2, row=4)
        self._profitLossValue = tk.Entry(self)
        self._profitLossValue.grid(column=2, row=5)

        self._feesLabel = tk.Label(self, text="Fees")
        self._feesLabel.grid(column=2, row=6)
        self._feesValue = tk.Entry(self)
        self._feesValue.grid(column=2, row=7)

        self.pack()

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
        except sqlite3.OperationalError:
            self._cursor.execute("CREATE TABLE journal_entries (id INTEGER PRIMARY KEY, data TEXT)")
            self._db.commit()

    def newEntry(self):
        return JournalEntry(self)

    def addEntry(self, jEntry):
        self._cursor.execute(self._insertStatements, (self._crypt.encryptBytes(jEntry.toJson()),) )
        jEntry.setId(self._cursor.lastrowid)
        self._entries.append(jEntry)

    def deleteEntry(self, jEntry):
        self._entries.remove(jEntry)
        self._cursor.execute(self._deleteStatement, (jEntry.getId(),))

    def getEntry(self):
        pass

    def updateEntry(self):
        pass

    def createNewEntry(self):
        rootWindow = tk.Toplevel(self.master)
        newEntryWindow = JournalEntryEditor(rootWindow, self)
