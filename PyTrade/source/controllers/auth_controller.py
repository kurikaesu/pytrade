from PyTrade.source.panels.auth_window import *


class AuthController:

    def __init__(self):

        self.__user = None
        self.__profile = None
        self.__auth_window = AuthWindow()
        if not self.__user:
            self.__auth_window.Signup()

    def sign_up(self):

        pass

    def sign_in(self):
        pass

