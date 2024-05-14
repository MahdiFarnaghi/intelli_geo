from datetime import datetime
import sqlite3


def getCurrentTimeStamp():
    currentTime = datetime.now()
    timeString = currentTime.strftime("%B %d %Y %H:%M:%S")

    return timeString


class Dataloader:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.databaseName)
        self.cursor = self.connection.cursor()

    def createtable(self, tablename):
        columns = ["sender TEXT", "time TEXT", "content TEXT"]

        createTableSql = f"CREATE TABLE IF NOT EXISTS {tablename} ({', '.join(columns)})"
        self.cursor.execute(createTableSql)
        self.connection.commit()

    def insertdata(self, tablename, sender, message):
        time = getCurrentTimeStamp()
        data = (sender, time, message)
        insert_sql = f"INSERT INTO {tablename} (sender, time, content) VALUES (?, ?, ?)"
        self.cursor.execute(insert_sql, data)
        self.connection.commit()

        return 'executed once'

    def selectdata(self, table_name, columns=None):
        if columns:
            select_sql = f"SELECT {', '.join(columns)} FROM {table_name}"
        else:
            select_sql = f"SELECT * FROM {table_name}"
        self.cursor.execute(select_sql)
        rows = self.cursor.fetchall()
        return rows

    def cleartable(self, tablename):
        clear_sql = f"DELETE FROM {tablename}"
        self.cursor.execute(clear_sql)
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
