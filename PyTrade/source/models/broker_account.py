from abc import ABCMeta


class BrokerAccount:
    __metaclass__ = ABCMeta
    __name = None
    __accountId = None
    __password = None

    def __init__(self, name):
        self.__name = name

    def setPassword(self, raw_password):
        pass

    # Use the passphrase of an user if logged in successfully
    def getPassword(self, passphrase):
        pass
