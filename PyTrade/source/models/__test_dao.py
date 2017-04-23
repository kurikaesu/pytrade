from PyTrade.source.models.model_dao import ModelDAO
from PyTrade.source.models.user import User

import sqlite3


db = sqlite3.connect("test.db")
username = b'bush@gmail.com'
password = b'ABC123'
password2 = b'CDE123'
dao = ModelDAO(db)
user = User(username)
user.set_password(password)
user.set_id(dao.save_object(user))
user.set_password(password2)
id = dao.find_entry_with_unique_value(user, 'username', username.decode())
dao.get_object(user, 1)
user.restore_from_data()