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
        self.__username = username
        self.__profile = -1

    @classmethod
    def load_user(cls,id ,username, encrypted_username, salt, profile_id):
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
        self.__crypt.setSalt(salt)
        self.__salt = salt

    def set_encrypted_name(self, encrypted_username):
        self.__encrypted_name = encrypted_username

    def get_username(self):
        return self.__username

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
        print(id)

    def get_data(self):
        return self.__data

    # Wrap user data into a structure for storing into db
    def save_data(self):
        if not self.__username:
            raise RuntimeWarning("Username is not set")
        if not self.__encrypted_name:
            raise RuntimeWarning("Username is not encrypted")
        if not self.__salt:
            raise RuntimeWarning("Salt is not created")
        if not self.__profile:
            raise RuntimeWarning("Profile in not initialised")

        # decode all values before storing them in db
        self.__data[self.COLUMN_HEADERS[self.USERNAME]] = self.__username.decode()
        self.__data[self.COLUMN_HEADERS[self.ENCRYPTED_NAME]] = self.__encrypted_name.decode()
        self.__data[self.COLUMN_HEADERS[self.SALT]] = self.__salt.decode()
        self.__data[self.COLUMN_HEADERS[self.PROFILE]] = self.__profile

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

    def set_profile(self, profile_id):
        self.__profile = profile_id
