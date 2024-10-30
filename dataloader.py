import copy
import sqlite3
import os
import json
import requests
import logging
from .utils import getCurrentTimeStamp, pack, unpack, tuple2Dict, getSystemInfo, captchaPopup


class Dataloader:
    def __init__(self, databaseName: str):
        self.databaseName = databaseName
        self.connection = None
        self.cursor = None
        self.llmFullDict = None
        self.llmEndpointDict = None
        self.apiKeyDict = None
        folderPath = os.path.expanduser("~/Documents/QGIS_IntelliGeo")
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        self.databasePath = os.path.join(folderPath, self.databaseName)

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

        # credential table
        self.credentialTableName = "credential"
        self.credentialTableColName = ["ID", "sessionID", "sessionKey"]

        # backend url
        self.backendURL = "https://owsgip.itc.utwente.nl/intelligeo/"

    def _checkExistence(self, tableName):
        """
        Checks whether a table with the specified name exists in the SQLite database.

        Args:
            tableName (str): The name of the table to check for existence.

        Returns:
            bool: `True` if the table exists, `False` otherwise.

        Example:
            >>> exists = self._checkExistence("users")
            # exists will be True if the "users" table exists, otherwise False.
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name = ? ;"
        self.cursor.execute(query, (tableName,))

        result = self.cursor.fetchone()

        # Return True if the table exists, False otherwise
        return result is not None

    def connect(self) -> None:
        """
        Connect and Initialization
        If there is no existing database then create one.
        """

        self.connection = sqlite3.connect(self.databasePath)
        self.cursor = self.connection.cursor()

        self._createLLMTable()
        self._createConversationTable()
        self._createPromptTable()
        self._createInteractionTable()
        self._createCrendentialTable()

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

        self.llmEndpointDict = dict()
        self.llmEndpointDict["OpenAI"] = "https://api.openai.com/v1/chat/completions"
        self.llmEndpointDict["Cohere"] = " https://api.cohere.com/v1/chat"
        self.llmEndpointDict["default"] = "default"

        self.apiKeyDict = dict()
        self.apiKeyDict["OpenAI"] = os.getenv("OPENAI_API_KEY", "")
        self.apiKeyDict["Cohere"] = os.getenv("COHERE_API_KEY", "")
        self.apiKeyDict["default"] = "default"

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
                    endpoint = self.llmEndpointDict[llmProvider]
                    apiKey = self.apiKeyDict[llmProvider]
                    rowToInsert.append([llmID, llmName, endpoint, apiKey])

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
                       f"FOREIGN KEY (conversationID) REFERENCES {self.conversationTableName}(ID)"
                       f"FOREIGN KEY (promptID) REFERENCES {self.promptTableName}(ID)"]

            createTableSql = f"CREATE TABLE IF NOT EXISTS {self.interactionTableName} ({', '.join(columns)})"
            self.cursor.execute(createTableSql)

            # create index on conversation ID
            createIndexSql = (f"CREATE INDEX IF NOT EXISTS idxConversationID"
                              f" ON {self.interactionTableName} (conversationID)")
            self.cursor.execute(createIndexSql)
            self.connection.commit()

    def _createCrendentialTable(self):
        if not self._checkExistence(self.credentialTableName):
            columns = ["ID TEXT PRIMARY KEY",
                       "sessionID TEXT",
                       "sessionKey TEXT"]
            createTableSql = f"CREATE TABLE IF NOT EXISTS {self.credentialTableName} ({', '.join(columns)})"
            self.cursor.execute(createTableSql)

    def getLLMInfo(self, llmID):
        provider, llmName = llmID.split("::", 1)
        if llmName in self.llmFullDict[provider]:
            return provider, llmName
        else:
            return "default", "default"

    def fetchPrompt(self, llmID, promptType):
        # fetchPromptSql = f"SELECT * FROM {self.promptTableName} WHERE llmID = ? AND promptType = ?"
        # self.cursor.execute(fetchPromptSql, (llmID, promptType))
        # allPromptRows = self.cursor.fetchall()
        # rows = tuple2Dict(allPromptRows, "prompt")
        # sortedRows = sorted(rows, key=lambda x: x["version"], reverse=True)
        params = {
            'llmID': 'Cohere::command-r-plus',
            'promptType': promptType
        }
        endpoint = f"{self.backendURL}/prompt_by/"
        # Send the GET request
        response = requests.get(endpoint, params=params)

        return response.json()

    def insertConversationInfo(self, conversationInfoDict):
        insertSQL = f"""
            INSERT INTO {self.conversationTableName} 
            (ID, llmID, title, description, created, modified, messageCount, workflowCount, userID) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        conversationInfoList = unpack(conversationInfoDict, "conversation")
        self.cursor.execute(insertSQL, conversationInfoList)
        self.connection.commit()

        self.postData("conversation", conversationInfoDict)

    def updateAPIKey(self, apiKey, ID):
        _, oldAPIKey = self.fetchAPIKey(ID)
        if oldAPIKey == apiKey:
            return

        updateSQL = f"""
            UPDATE {self.llmTableName}
            SET apiKey = ? WHERE ID = ?
            """

        self.cursor.execute(updateSQL, (apiKey, ID))
        self.connection.commit()

    def fetchAPIKey(self, ID) -> tuple[str, str]:
        fetchSQL = f"""
            SELECT endpoint, apiKey FROM {self.llmTableName}
            WHERE ID = ?
            """
        self.cursor.execute(fetchSQL, (ID,))
        result = self.cursor.fetchone()

        if result:
            endpoint, apiKey = result
            return endpoint, apiKey
        else:
            raise ValueError(f"No record found with ID: {ID}", ID)

    def fetchAllConfig(self):
        fetchSQL = f"""
            SELECT * FROM {self.llmTableName}
            """
        self.cursor.execute(fetchSQL)
        rows = self.cursor.fetchall()

        return rows

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

    def loadCredential(self):
        querySQL = f"SELECT * FROM {self.credentialTableName} ORDER BY ID LIMIT 1"
        self.cursor.execute(querySQL)
        row = self.cursor.fetchone()
        if row is not None:
            return row[1], row[2]
        else:
            return "", ""

    def updateCredential(self, sessionID, sessionKey):
        self.cursor.execute(f"SELECT ID FROM {self.credentialTableName} ORDER BY ID LIMIT 1")
        row = self.cursor.fetchone()
        if row:
            # Row exists, update it
            self.cursor.execute(f"UPDATE {self.credentialTableName} SET sessionID = ?, sessionKey = ? WHERE ID = ?",
                           (sessionID, sessionKey, row[0]))
        else:
            # No row exists, insert a new row
            new_id = "1"
            self.cursor.execute(f"INSERT INTO {self.credentialTableName} (ID, sessionID, sessionKey) VALUES (?, ?, ?)",
                           (new_id, sessionID, sessionKey))

        self.connection.commit()

    def createConversation(self, metaInfo):
        self.insertConversationInfo(metaInfo)

    def deleteConversation(self, conversationID):
        self.deleteConversationInfo(conversationID)

        deleteSQL = f"DELETE from {self.interactionTableName} WHERE conversationID = ?"
        self.cursor.execute(deleteSQL, (conversationID,))

    def insertInteraction(self, interactionInfo: tuple, conversationID: str) -> str:
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

        interactionDict = pack(interaction, "interaction")
        self.postData("interaction", interactionDict)

        return interactionIndex

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

    def selectLatestInteraction(self, conversationID, interactionID=None):
        if interactionID is not None:
            selectSQL = (f"SELECT * FROM {self.interactionTableName} "
                         f"WHERE conversationID = ? AND ID = ?")
            self.cursor.execute(selectSQL, (conversationID, interactionID))
            row = self.cursor.fetchone()
            if row is not None:
                return row

        rows = self.selectInteraction(conversationID)
        processedRows = []
        for row in rows:
            packedRow = pack(row, "interaction")
            if packedRow["conversationID"] in packedRow["ID"]:
                processedRows.append(list(row) + [int(packedRow["ID"][len(packedRow["conversationID"]):])])

        sortedRows = sorted(processedRows, key=lambda x: x[-1])
        return sortedRows[-1][:-1]

    def postData(self, endpoint, data):
        payload = data
        header = getSystemInfo()

        while True:
            dataDict = copy.deepcopy(data)
            sessionID, sessionKey = self.loadCredential()
            dataDict["sessionID"] = sessionID
            dataDict["sessionKey"] = sessionKey
            try:
                response = requests.post(f"{self.backendURL}/{endpoint}", json=dataDict, headers=header)
                if response.status_code == 200:
                    break
                else:
                    errorResponse = response.json()
                    captchaDict = errorResponse.get('detail', {})
                    answer = captchaPopup(captchaDict)
                    body = {"answer": answer}

                    header = getSystemInfo()
                    header["sendtime"] = getCurrentTimeStamp()

                    response = requests.post(f"{self.backendURL}/register", headers=header, json=body)
                    if response.status_code == 200:
                        response_data = response.json()

                        # Extract the credentials
                        sessionID = response_data.get("sessionID")
                        sessionKey = response_data.get("sessionKey")
                        self.updateCredential(sessionID, sessionKey)

            except requests.exceptions.HTTPError as httpErr:
                continue

    def updateData(self, endpoint, ID, data):
        response = requests.put(f"{self.backendURL}/{endpoint}/{ID}", json=data)

    def close(self):
        if self.connection:
            self.connection.close()
