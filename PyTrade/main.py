from source import *
import sqlite3

if __name__ == "__main__":
    db = sqlite3.connect("data.db")
    crypto = Crypt()
    crypto.setSalt(b'3\xdaz\x00\xd0q\xb5R>\x1e\\Nz\xaa8\xfe')
    crypto.initWithPassword(b'ABC123')
    app = Application(None, crypto, db)
    app.setBrokerPlugins(brokers.broker_base.brokerPluginList)
    app.mainloop()
