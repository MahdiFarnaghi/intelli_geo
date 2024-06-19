import sqlite3
from .utils import getCurrentTimeStamp, unpack, show_variable_popup


class Dataloader:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.connection = None
        self.cursor = None

        self.metaTableName = None
        self.metaTableColNames = ['title', 'description', 'created', 'lastEdit', 'LLMName', 'messageCount',
                                  'modelCount', 'ID']

    def connect(self):
        self.connection = sqlite3.connect(self.databaseName)
        self.cursor = self.connection.cursor()

    def createMetaTable(self):
        if self.metaTableName is None:
            columns = ["title TEXT, description TEXT, created TEXT, lastEdit TEXT, "
                       "LLMName TEXT, messageCount INT, modelCount INT, ID TEXT"]
            self.metaTableName = 'Metatable'
            createTableSql = f"CREATE TABLE IF NOT EXISTS {self.metaTableName} ({', '.join(columns)})"
            self.cursor.execute(createTableSql)
            self.connection.commit()

    def insertMetaInfo(self, metaInfo):
        insertSQL = """
            INSERT INTO Metatable 
            (title, description, created, lastEdit, LLMName, messageCount, modelCount, ID) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
        metaInfoList = [metaInfo[col] for col in self.metaTableColNames]
        self.cursor.execute(insertSQL, metaInfoList)
        self.connection.commit()

    def selectMetaInfo(self, ID=None):
        if self.metaTableName is None:
            rows = []
        else:
            if ID is None:
                selectSQL = f"SELECT * FROM Metatable"
                self.cursor.execute(selectSQL)
            else:
                selectSQL = "SELECT * FROM Metatable WHERE ID = ?"
                self.cursor.execute(selectSQL, (ID,))
            rows = self.cursor.fetchall()

        result = []
        for row in rows:
            rowDict = {}
            for i, column_name in enumerate(self.metaTableColNames):
                rowDict[column_name] = row[i]
            result.append(rowDict)

        return result

    def deleteMetaInfo(self, ID):
        deleteSQL = "DELETE FROM Metatable WHERE ID = ?"
        self.cursor.execute(deleteSQL, (ID,))
        self.connection.commit()

    def updateMetaInfo(self, metaInfo):
        (title,
         description,
         created,
         lastEdit,
         LLMName,
         messageCount,
         modelCount,
         ID) = unpack(metaInfo)
        updateSQL = ("UPDATE Metatable SET title = ?, description = ?, lastEdit = ?, messageCount = ?, modelCount = ? "
                     "WHERE ID = ?")
        self.cursor.execute(updateSQL, (title, description, lastEdit, messageCount, modelCount, ID))
        self.connection.commit()

    def createTable(self, metaInfo):
        tableID = metaInfo['ID']
        self.insertMetaInfo(metaInfo)

        # create table
        columns = ["sender TEXT", "time TEXT", "content TEXT", "model TEXT"]

        createTableSql = f"CREATE TABLE IF NOT EXISTS {tableID} ({', '.join(columns)})"
        self.cursor.execute(createTableSql)
        self.connection.commit()

    def dropTable(self, tableID):
        dropTableSQL = f"DROP TABLE IF EXISTS {tableID}"
        if self.cursor is not None:
            self.cursor.execute(dropTableSQL)
            self.connection.commit()

            self.deleteMetaInfo(tableID)

    def insertData(self, tableID, sender, message, model=''):
        time = getCurrentTimeStamp()
        data = (sender, time, message, model)
        insertSQL = f"INSERT INTO {tableID} (sender, time, content, model) VALUES (?, ?, ?, ?)"
        self.cursor.execute(insertSQL, data)
        self.connection.commit()

        return 'executed once'

    def selectData(self, tableID, columns=None):
        if columns:
            selectSQL = f"SELECT {', '.join(columns)} FROM {tableID}"
        else:
            selectSQL = f"SELECT * FROM {tableID}"
        self.cursor.execute(selectSQL)
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        if self.connection:
            self.connection.close()
