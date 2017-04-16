import sqlite3

class ModelDAO:

    CREATE_TABLE_STATEMENT = "CREATE TABLE IF NOT EXISTS %s (%s)"
    INSERT_STATEMENT = "INSERT INTO %s(%s) VALUES (%s)"
    UPDATE_STATEMENT = "UPDATE %s SET %s WHERE %s"

    PRIMARY_KEY = "PRIMARY KEY"
    NOT_NULL = "NOT NULL"
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    HEADERS = "column_headers"

    __db = None

    def __init__(self, db):
        self.__db = db
        pass

    def __check_table_exist(self, model):
        table_name = model.__class__.__name__
        attributes = 'id %s %s ' % (self.INTEGER, self.PRIMARY_KEY)
        data = model.get_data()
        for header in data['column_headers']:
            attributes += ',%s %s %s ' % (header, self.TEXT, self.NOT_NULL)

        statement = self.CREATE_TABLE_STATEMENT % (table_name, attributes)
        print(statement)
        return table_name

    def save_object(self, model):
        # create a table if table is not exist
        table_name = self.__check_table_exist(model)
        data = model.get_data()
        columns = data[self.HEADERS]
        where_clause = 'id = %s' % model.get_id()

        # First of all, do update before insert



        # print(attributes)


        pass

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
