import tkinter as tk
import tkinter.ttk as ttk

import json

class JournalEntry:
    def __init__(self, parentJournal = None, preData = None):
        self._parentJournal = parentJournal

        if preData == None:
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

class Journal(tk.Frame):
    def __init__(self, parent, db, crypt):
        super(Journal, self).__init__(parent)
        self._entries = []
        self._db = db
        self._cursor = self._db.cursor()
        self._crypt = crypt

    def loadEntries(self):
        for row in self._cursor.execute("SELECT data FROM journal_entries ORDER BY id ASC"):
            data = json.loads(self._crypt.decryptBytes(row[0]))
            self._entries.append(JournalEntry(self, data))

    def newEntry(self):
        return JournalEntry(self)

    def addEntry(self, jEntry):
        self._entries.append(jEntry)

    def deleteEntry(self, jEntry):
        self._entries.remove(jEntry)

    def getEntry(self):
        pass

    def updateEntry(self):
        pass
