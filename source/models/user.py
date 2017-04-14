from source.core import *


class User:
    # variables to be stored in db
    __id = None
    __username = None
    __encrypted_name = None
    __salt = None
    __profile = None

    # variables for runtime
    __crypt = None

    def __init__(self, username):
        self.__username = username
        self.__load_profile_from_db()

    @classmethod
    def load_user(cls, username, encrypted_username, salt):
        user = cls(username)
        user.set_salt(salt)
        user.set_encrypted_name(encrypted_username)

        return cls(username)

    def set_salt(self, salt=None):
        self.__crypt = Crypt()
        if not salt:
            salt = Crypt.gen_salt()
        self.__crypt.setSalt(salt)
        self.__salt = salt

    def set_encrypted_name(self, encrypted_username):
        self.__encrypted_name = encrypted_username

    def get_username(self):
        return self.__username

    def set_password(self, raw_password):
        self.set_salt()
        self.__crypt.initWithPassword(raw_password)
        self.__encrypted_name = self.__crypt.encryptBytes(self.get_username())
        pass

    def validate_password(self, raw_password):
        if not self.__salt:
            raise RuntimeWarning("Password is not set")
        res = self.__crypt.validatePassword(
            raw_password,
            self.__encrypted_name,
            self.__username
        )
        if res:
            return True
        else:
            return False

    def get_profile(self):
        pass

    def __load_profile_from_db(self):
        pass



