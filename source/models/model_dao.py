
class ModelDAO:

    __db = None

    __insertStatement = "INSERT INTO %s(%s) VALUES (%s)"
    __updateStatement = ""

    def __init__(self, db):
        self.__db = db
        pass

    def save_object(self, model):
        table_name = model.__class__.__name__
        columns = model.get_data()
        for header in columns['column_headers']:
            print(header)

        return model.__class__.__name__

    def save_all_objects(self, objs):
        pass

    def get_all_objects(self):
        # try:
        #     for row in self._cursor.execute("SELECT id, data FROM journal_entries ORDER BY id ASC"):
        #         entry = JournalEntry(self, row[0])
        #         entry.fromJson(self._crypt.decryptBytes(row[1]))
        #         self._entries.append(entry)
        #         self._journalList.insert('', 'end', values=entry.asListRow())
        # except sqlite3.OperationalError:
        #     self._cursor.execute("CREATE TABLE journal_entries (id INTEGER PRIMARY KEY, data TEXT)")
        #     self._db.commit()

        pass
