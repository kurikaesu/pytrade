from ..core import *


class User:

    # Data header indexes
    USERNAME = 0
    ENCRYPTED_NAME = 1
    SALT = 2
    PROFILE = 3

    # data header in the user table
    COLUMN_HEADERS = [
        'username',
        'encrypted_name',
        'salt',
        'profile',
    ]

    # variables to be stored in db
    __id = None
    __username = None
    __encrypted_name = None
    __salt = None
    __profile = None

    # variables for runtime
    __crypt = None
    __data = {'column_headers': COLUMN_HEADERS}

    def __init__(self, username):
        self.set_username(username)
        self.set_profile(-1)

    @classmethod
    def load_user(cls, id, username, encrypted_username, salt, profile_id):
        user = cls(username.encode())
        user.set_id(id)
        user.set_salt(salt.encode())
        user.set_encrypted_name(encrypted_username.encode())
        user.set_profile(int(profile_id))

        return cls(username)

    def set_salt(self, salt=None):
        self.__crypt = Crypt()
        if not salt:
            salt = Crypt.gen_salt()
        salt = self.__to_bstring(salt)
        self.__crypt.setSalt(salt)
        self.__salt = salt
        self.__data[self.COLUMN_HEADERS[self.SALT]] = self.__to_string(salt)

    def set_encrypted_name(self, encrypted_username):
        self.__encrypted_name = self.__to_bstring(encrypted_username)
        self.__data[self.COLUMN_HEADERS[self.ENCRYPTED_NAME]] = self.__to_string(encrypted_username)

    def set_username(self, username):
        self.__username = self.__to_bstring(username)
        self.__data[self.COLUMN_HEADERS[self.USERNAME]] = self.__to_string(self.__username)

    def get_username(self):
        return self.__to_string(self.__username)

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_data(self):
        return self.__data

    # Wrap user data into a structure for storing into db
    def set_data(self, data):
        self.__data = data
        pass

    def restore_from_data(self):
        self.set_encrypted_name(self.__data[self.COLUMN_HEADERS[self.ENCRYPTED_NAME]])
        self.set_salt(self.__data[self.COLUMN_HEADERS[self.SALT]])

    def set_password(self, raw_password):
        self.set_salt()
        self.__crypt.initWithPassword(self.__to_bstring(raw_password))
        self.set_encrypted_name(self.__crypt.encryptBytes(self.__username))
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

    def set_profile(self, profile_id):
        self.__profile = profile_id
        self.__data[self.COLUMN_HEADERS[self.PROFILE]] = profile_id

    def __to_bstring(self, data):
        try:
            data = data.encode()
        except AttributeError:
            pass
        return data

    def __to_string(self, data):
        try:
            data = data.decode()
        except AttributeError:
            pass
        return data
