from ..core import *


class User:
    __id = None
    __username = None
    __password = None
    __salt = None
    __profile = None
    __crypt = None

    def __init__(self, username):
        self.__crypt = Crypt()
        self.__username = username
        self.__salt = Crypt.gensalt()
        self.__load_profile_from_db()

    @classmethod
    def load_user(cls, username, encrypted_pw, salt):
        pass

    def __set_crypt(self, encrypted_pw, salt):
        pass

    def get_username(self):
        return self.__username

    def set_password(self, raw_password):
        pass

    def get_password(self):
        pass

    def get_profile(self):
        pass

    def __load_profile_from_db(self):
        pass



