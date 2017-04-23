from tkinter import *
from PyTrade.source.models import *


class AuthController:

    def __init__(self, view, dao):

        self.__user = None
        self.__profile = None
        self.__auth_view = view
        self.__data_access_o = dao
        view.sign_up_button.config(command=self.sign_up)
        view.sign_in_button.config(command=self.sign_in)
        pass

    def sign_up(self):
        user = User(self.__auth_view.get_username())
        user.set_password(self.__auth_view.get_password())
        user.set_id(self.__data_access_o.save_object(user))
        self.__user = user
        pass

    def sign_in(self):
        print("sign in")
        username = self.__auth_view.get_username()
        password = self.__auth_view.get_password()
        user = User(username)
        id = self.__data_access_o.find_entry_with_unique_value(user, 'username', username)
        if id:
            print("find %d" % id)
            self.__data_access_o.get_object(user, id)
        else:
            print("couldn't find")
            return
        user.restore_from_data()
        user.set_id(id)
        if user.validate_password(password.encode()):
            print("success")
        else:
            print("failed")
        pass

    def get_user(self):
        return self.__user

