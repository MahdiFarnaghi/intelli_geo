import sqlite3
import os
import json
from .utils import getCurrentTimeStamp, unpack, show_variable_popup, tuple2Dict


class Dataloader:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.connection = None
        self.cursor = None
        self.llmFullDict = None

        # llm table
        self.llmTableName = "llm"
        self.llmTableColname = ["ID", "name", "endpoint", "apiKey"]

        # prompt table
        self.promptTableName = "prompt"
        self.promptTableColname = ["ID", "llmID", "version", "template", "promptType"]

        # conversation table
        self.conversationTableName = "conversation"
        self.conversationTableColname = ["ID", "llmID", "title", "description", "created", "modified", "userID"]

        # interaction table
        self.interactionTableName = "interaction"
        self.interactionTableColname = ["ID", "conversationID", "promptID", "requestText", "contextText", "requestTime",
                                        "typeMessage", "responseText", "responseTime", "workflow", "executionLog"]

    def _checkExistence(self, tableName):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name = ? ;"
        self.cursor.execute(query, (tableName,))

        result = self.cursor.fetchone()

        # Return True if the table exists, False otherwise
        return result is not None

    def connect(self) -> None:
        """
        Connect and Initialization
        """
        self.connection = sqlite3.connect(self.databaseName)
        self.cursor = self.connection.cursor()

        self._createLLMTable()
        self._createConversationTable()
        self._createPromptTable()
        self._createInteractionTable()

    def _createLLMTable(self):
        """
        Create "llm" table if d not exist and insert "llm ID" and "llm ame".
        Each row in table should look like: Cohere::command-r-plus, command-r-plus, ..., ...
        """
        # Full dict of llm names and providers. Will be used in `.getLLMInfo()`
        self.llmFullDict = dict()
        self.llmFullDict["Cohere"] = ["command-r-plus", "command-r", "command", "command-nightly",
                                      "command-light", "command-light-nightly"]
        self.llmFullDict["OpenAI"] = ["gpt-4", "gpt-3.5-turbo"]
        self.llmFullDict["default"] = ["default"]

        if not self._checkExistence(self.llmTableName):
            columns = ["ID TEXT NOT NULL PRIMARY KEY",
                       "name TEXT NOT NULL",
                       "endpoint TEXT",
                       "apiKey TEXT"]

            creationSQL = f"CREATE TABLE IF NOT EXISTS {self.llmTableName} ({', '.join(columns)})"
            self.cursor.execute(creationSQL)

            rowToInsert = []
            for llmProvider, llmNameList in self.llmFullDict.items():
                for llmName in llmNameList:
                    llmID = f"{llmProvider}::{llmName}"
                    rowToInsert.append([llmID, llmName, None, None])

            self.cursor.executemany(f"""
                INSERT INTO {self.llmTableName} (ID, name, endpoint, apiKey)
                VALUES (?, ?, ?, ?)
                """, rowToInsert)
            self.connection.commit()

    def _createPromptTable(self) -> None:
        """
        Create "prompt" table if not exist and insert "ID".
        Each row in the table should be like:
            Cohere::command-r-plus::0::generalChat;
            Cohere::command-r-plus;
            0;
            ...;
            generalChat;
        """
        if not self._checkExistence(self.promptTableName):
            columns = ["ID TEXT NOT NULL PRIMARY KEY",
                       "llmID TEXT NOT NULL",
                       "version INTEGER NOT NULL",
                       "template TEXT NOT NULL",
                       "promptType TEXT NOT NULL",
                       f"FOREIGN KEY (llmID) REFERENCES {self.llmTableName}(ID)"]
            creationSQL = f"CREATE TABLE IF NOT EXISTS {self.promptTableName} ({', '.join(columns)})"
            self.cursor.execute(creationSQL)

            # TODO: Temporary solution!
            currentFilePath = os.path.abspath(__file__)
            currentFolder = os.path.dirname(currentFilePath)
            promptPath = os.path.join(currentFolder, "resources", "prompt_v0.1.json")
            with open(promptPath, 'r') as file:
                promptDict = json.load(file)

            rowToInsert = []
            for promptType in promptDict:
                for llmProvider in promptDict[promptType]:
                    for llmName in self.llmFullDict[llmProvider]:
                        promptID = f"{llmProvider}::{llmName}::0::{promptType}"
                        llmID = f"{llmProvider}::{llmName}"
                        version = 0
                        template = ""
                        for key, value in promptDict[promptType][llmProvider].items():
                            template += key + ":\n\n" + value + "\n\n"

                        rowToInsert.append([promptID, llmID, version, template, promptType])

            self.cursor.executemany(f"""
                            INSERT INTO {self.promptTableName} (ID, llmID, version, template, promptType)
                            VALUES (?, ?, ?, ?, ?)
                            """, rowToInsert)
            self.connection.commit()

    def _createConversationTable(self):
        if not self._checkExistence(self.conversationTableName):
            columns = ["ID TEXT NOT NULL PRIMARY KEY",
                       "llmID TEXT NOT NULL",
                       "title TEXT NOT NULL",
                       "description TEXT NOT NULL",
                       "created TEXT NOT NULL",
                       "modified TEXT NOT NULL",
                       "messageCount INT NOT NULL",
                       "workflowCount INT NOT NULL",
                       "userID TEXT NOT NULL",
                       f"FOREIGN KEY (llmID) REFERENCES {self.llmTableName}(ID)"]
            createTableSql = f"CREATE TABLE IF NOT EXISTS {self.conversationTableName} ({', '.join(columns)})"
            self.cursor.execute(createTableSql)
            self.connection.commit()

    def _createInteractionTable(self):
        if not self._checkExistence(self.interactionTableName):
            columns = ["ID TEXT PRIMARY KEY",
                       "conversationID TEXT NOT NULL",
                       "promptID TEXT NOT NULL",
                       "requestText TEXT NOT NULL",
                       "contextText TEXT NOT NULL",
                       "requestTime TEXT NOT NULL",
                       "typeMessage TEXT NOT NULL",
                       "responseText TEXT",
                       "responseTime TEXT",
                       "workflow TEXT",
                       "executionLog TEXT",
                       f"FOREIGN KEY (conversationID) REFERENCES {self.conversationTableName}(ID)"]

            createTableSql = f"CREATE TABLE IF NOT EXISTS {self.interactionTableName} ({', '.join(columns)})"
            self.cursor.execute(createTableSql)

            # create index on conversation ID
            createIndexSql = (f"CREATE INDEX IF NOT EXISTS idxConversationID"
                              f" ON {self.interactionTableName} (conversationID)")
            self.cursor.execute(createIndexSql)
            self.connection.commit()

    def getLLMInfo(self, llmID):
        provider, llmName = llmID.split("::", 1)
        if llmName in self.llmFullDict[provider]:
            return provider, llmName
        else:
            return "default", "default"

    def fetchPrompt(self, llmID, promptType):
        show_variable_popup(llmID)
        show_variable_popup(promptType)
        fetchPromptSql = f"SELECT * FROM {self.promptTableName} WHERE llmID = ? AND promptType = ?"
        self.cursor.execute(fetchPromptSql, (llmID, promptType))
        allPromptRows = self.cursor.fetchall()
        show_variable_popup(allPromptRows)
        rows = tuple2Dict(allPromptRows, "prompt")
        sortedRows = sorted(rows, key=lambda x: x["version"], reverse=True)

        return sortedRows[0]

    def insertConversationInfo(self, conversationInfoDict):
        insertSQL = f"""
            INSERT INTO {self.conversationTableName} 
            (ID, llmID, title, description, created, modified, messageCount, workflowCount, userID) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        conversationInfoList = unpack(conversationInfoDict, "conversation")
        self.cursor.execute(insertSQL, conversationInfoList)
        self.connection.commit()

    def selectConversationInfo(self, conversationID=None):
        if self.conversationTableName is None:
            rowList = []
        else:
            if conversationID is None:
                selectSQL = f"SELECT * FROM {self.conversationTableName}"
                self.cursor.execute(selectSQL)
                rowList = tuple2Dict(self.cursor.fetchall(), "conversation")
            else:
                selectSQL = f"SELECT * FROM {self.conversationTableName} WHERE ID = ?"
                self.cursor.execute(selectSQL, (conversationID,))
                rowList = tuple2Dict(self.cursor.fetchall(), "conversation")
                show_variable_popup(conversationID)

            for row in rowList:
                rowConversationID = row["ID"]

                # Query to count rows with a specific conversationID
                messageCountQuery = (f"SELECT COUNT(*) FROM {self.interactionTableName} WHERE conversationID = ?"
                                     f"AND typeMessage != 'internal'")
                self.cursor.execute(messageCountQuery, (rowConversationID,))
                row["messageCount"] = self.cursor.fetchone()[0]

                # Query to count rows with a specific conversationID and non-empty workflow
                workflowCountQuery = (f"SELECT COUNT(*) FROM {self.interactionTableName} WHERE conversationID = ?"
                                      f"AND workflow != 'empty'")
                self.cursor.execute(workflowCountQuery, (rowConversationID,))
                row["workflowCount"] = self.cursor.fetchone()[0]

        return rowList if conversationID is None else rowList[0]

    def deleteConversationInfo(self, conversationID):
        deleteSQL = f"DELETE FROM {self.conversationTableName} WHERE ID = ?"
        self.cursor.execute(deleteSQL, (conversationID,))
        self.connection.commit()

    def updateConversationInfo(self, metaInfo: dict) -> None:
        """
        Update row in "conversation" table
        """
        (conversationID,
         llmID,
         title,
         description,
         created,
         modified,
         messageCount,
         workflowCount,
         userID) = unpack(metaInfo, "conversation")
        updateSQL = (f"UPDATE {self.conversationTableName} SET llmID = ?, title = ?, description = ?, "
                     f"created = ?, modified = ?, messageCount = ?, workflowCount = ?, userID = ? WHERE ID = ?")
        self.cursor.execute(updateSQL,
                            (llmID, title, description, created, modified,
                             messageCount, workflowCount, userID, conversationID))
        self.connection.commit()

    def createConversation(self, metaInfo):
        self.insertConversationInfo(metaInfo)

    def deleteConversation(self, conversationID):
        self.deleteConversationInfo(conversationID)

        deleteSQL = f"DELETE from {self.interactionTableName} WHERE conversationID = ?"
        self.cursor.execute(deleteSQL, (conversationID,))

    def insertInteraction(self, interactionInfo, conversationID):
        # Get interaction index
        messageCountQuery = (f"SELECT COUNT(*) FROM {self.interactionTableName} WHERE conversationID = ?"
                             f"AND typeMessage != 'internal'")
        self.cursor.execute(messageCountQuery, (conversationID,))
        interactionIndex = conversationID + str(self.cursor.fetchone()[0])

        # Insert row into "interaction" tablet
        allColname = ", ".join(self.interactionTableColname)
        insertSQL = (f"INSERT INTO {self.interactionTableName} ({allColname}) "
                     f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        interaction = tuple([interactionIndex] + interactionInfo)

        self.cursor.execute(insertSQL, interaction)
        self.connection.commit()

    def selectInteraction(self, conversationID, columns=None):
        if columns:
            selectSQL = (f"SELECT {', '.join(columns)} FROM {self.interactionTableName} "
                         f"WHERE conversationID = ? AND typeMessage = ?")
        else:
            selectSQL = (f"SELECT * FROM {self.interactionTableName} "
                         f"WHERE conversationID = ? AND typeMessage IN (?, ?)")
        self.cursor.execute(selectSQL, (conversationID, "input", "return"))
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        if self.connection:
            self.connection.close()
