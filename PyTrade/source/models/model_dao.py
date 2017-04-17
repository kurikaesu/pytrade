

class ModelDAO:

    GET_MAX_ID_OF_TABLE = "SELECT MAX(id) FROM %s;"
    CREATE_TABLE_STATEMENT = "CREATE TABLE IF NOT EXISTS %s (%s)"
    INSERT_STATEMENT = "INSERT INTO %s(%s) VALUES (%s)"
    UPDATE_STATEMENT = "UPDATE %s SET %s"
    SELECT_STATEMENT = "SELECT %s FROM %s"
    WHERE_CLAUSE = "WHERE"
    CANNOT_FIND = -1

    PRIMARY_KEY = "PRIMARY KEY"
    NOT_NULL = "NOT NULL"
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    HEADERS = "column_headers"

    __db = None
    __cursor = None

    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()
        pass

    def __execute_sql(self, sql_statement):
        try:
            res = self.__cursor.execute(sql_statement)
        except Exception as e:
            raise RuntimeWarning(e)
        return res

    def __get_max_id(self, table_name):
        statement = self.GET_MAX_ID_OF_TABLE % table_name
        rows = self.__execute_sql(statement)
        res = rows.fetchone()
        next_id = res[0] + 1
        return next_id

    def __create_table_if_not_exist(self, model):
        table_name = model.__class__.__name__
        attributes = 'id %s %s ' % (self.INTEGER, self.PRIMARY_KEY)
        data = model.get_data()
        for header in data['column_headers']:
            attributes += ',%s %s %s ' % (header, self.TEXT, self.NOT_NULL)

        statement = self.CREATE_TABLE_STATEMENT % (table_name, attributes)
        self.__execute_sql(statement)
        return table_name

    def __generate_update_statement(self, table_name, headers, data,  id):
        where_clause = '%s id = %s' % (self.WHERE_CLAUSE, id)
        attributes = []
        for header in headers:
            if data[header]:
                attributes.append("%s = '%s'" % (header, data[header]))
        set_clause = ', '.join(attributes)
        print(set_clause)
        print(where_clause)
        return '%s %s' % (self.UPDATE_STATEMENT % (table_name, set_clause), where_clause)

    def __generate_create_statement(self, table_name, headers, data):
        values = []
        attributes = []
        for header in headers:
            if data[header]:
                attributes.append(header)
                values.append("'%s'" % data[header])

        header_clause = ', '.join(attributes)
        value_clause = ', '.join(values)
        return self.INSERT_STATEMENT % (table_name, header_clause, value_clause)

    def find_entry_with_unique_value(self, model, key, value):
        table_name = model.__class__.__name__
        where_clause = '%s %s=%s' % (self.WHERE_CLAUSE, key, ('"%s"' % value))
        select_statement = '%s %s' % (self.SELECT_STATEMENT % ('id', table_name), where_clause)
        rows = self.__execute_sql(select_statement)
        res = rows.fetchone()
        return res[0]

    def save_object(self, model):
        # create a table if table is not exist
        table_name = self.__create_table_if_not_exist(model)
        id = model.get_id()
        data = model.get_data()
        headers = data[self.HEADERS]

        if id:
            statement = self.__generate_update_statement(table_name, headers, data, id)
            print(statement)
        else:
            statement = self.__generate_create_statement(table_name, headers, data)
            print(statement)

        try:
            self.__execute_sql(statement)
            self.__db.commit()
            new_id = self.__cursor.lastrowid
            if new_id:
                return new_id
            else:
                return id
        except:
            return self.CANNOT_FIND
