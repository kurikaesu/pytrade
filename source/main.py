from apis import *

from panels import *

if __name__ == "__main__":
    app = Application()
    app.setBrokerPlugins(brokers.broker_base.brokerPluginList)
    app.mainloop()
