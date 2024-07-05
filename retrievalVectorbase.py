import requests
import faiss
import re
import os
import json
import csv
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLSectionSplitter

from .utils import readURL, splitAtPattern


class RetrievalVectorbase:
    def __init__(self, version):
        self.version = version
        self.embeddingModel = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectorStorePath = os.path.join(os.path.expanduser("~"), "Documents", "QGIS_IntelliGeo", ".vectorDB")
        os.makedirs(self.vectorStorePath, exist_ok=True)

        # Load/Create vector store for PyQgis document
        self.documentStorePath = os.path.join(self.vectorStorePath, f"Document_{version}.faiss")
        self.documentContentPath = os.path.join(self.vectorStorePath, f"Document_{version}.json")
        if not os.path.exists(self.documentStorePath) or not os.path.exists(self.documentContentPath):
            self.createDocumentStore()

        self.documentVectorStore = faiss.read_index(self.documentStorePath)
        with open(self.documentContentPath, 'r') as file:
            self.documentContent = json.load(file)

        # Load/Create vector store for few-shot examples
        self.fewshotStorePath = os.path.join(self.vectorStorePath, f"Fewshot_{version}.faiss")
        self.fewshotContentPath = os.path.join(self.vectorStorePath, f"Fewshot_{version}.json")
        if not os.path.exists(self.fewshotStorePath) or not os.path.exists(self.fewshotContentPath):
            self.createFewshotStore()

        self.fewshotVectorStore = faiss.read_index(self.fewshotStorePath)
        with open(self.fewshotContentPath, 'r') as file:
            self.fewshotContent = json.load(file)

    def createDocumentStore(self) -> None:
        cookbookPrefixURL = f"https://docs.qgis.org/{self.version}/en/docs/pyqgis_developer_cookbook/"
        functionListURL = f"https://docs.qgis.org/{self.version}/en/docs/user_manual/expressions/functions_list.html"

        cookbookURL = self._getCookbookURL(cookbookPrefixURL)
        cookbookDocument = []
        for url in cookbookURL:
            cookbookDocument.append(readURL(url))

        functionListContent = readURL(functionListURL)
        fullDocument = cookbookDocument + splitAtPattern(functionListContent)
        with open(self.documentContentPath, 'w') as file:
            json.dump(fullDocument, file)

        docEmbedding = self.embeddingModel.encode(fullDocument)
        dimension = docEmbedding.shape[1]

        faissIndex = faiss.IndexFlatL2(dimension)
        faissIndex.add(docEmbedding)
        faiss.write_index(faissIndex, self.documentStorePath)

    def createFewshotStore(self) -> None:
        # TODO: To be changed later after the server/local side decision
        currentFilePath = os.path.abspath(__file__)
        currentFolder = os.path.dirname(currentFilePath)
        exampleMapPath = os.path.join(currentFolder, "resources", "Model_examples", "few_shot_examples.csv")

        # load the few-shot examples
        workflowList, userInputList = [], []
        with open(exampleMapPath, "r", newline='') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                workflowList.append(str(row[0]))
                userInputList.append(' '.join(row[1:]))

        # Encode the user query to embedding
        inputEmbedding = self.embeddingModel.encode(userInputList)
        dimension = inputEmbedding.shape[1]

        # Create Faiss index with L2-norm
        faissIndex = faiss.IndexFlatL2(dimension)
        faissIndex.add(inputEmbedding)
        faiss.write_index(faissIndex, self.fewshotStorePath)

        fewshotContent = []
        for i, workflow in enumerate(workflowList):
            # Read model files

            fewshotContent.append(dict())
            modelPath = os.path.join(currentFolder, "resources", "Model_examples", "Models", f"{workflow}.model3")
            with open(modelPath, "r") as file:
                fewshotContent[i]["Model"] = "\n\n" + userInputList[i] + ":\n\n" + file.read()

            # Read script files
            scriptPath = os.path.join(currentFolder, "resources", "Model_examples", "Scripts", f"{workflow}.py")
            with open(scriptPath, "r") as file:
                fewshotContent[i]["Script"] = "\n\n" + userInputList[i] + ":\n\n" + file.read()

        with open(self.fewshotContentPath, 'w') as file:
            json.dump(fewshotContent, file, indent=4)

    def _getCookbookURL(self, cookbookPrefixURL: str) -> list[str]:
        response = requests.get(cookbookPrefixURL)
        docLink = []
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        clickable_links = [link.get('href') for link in links if link.get('href')]

        # Print the clickable links
        for link in set(clickable_links):
            if link[:6] == "https:":
                continue
            elif link[0] == ".":
                continue
            elif '#' in link:
                continue
            docLink.append(cookbookPrefixURL + link)

        return docLink

    def retrieveDocument(self, userInput, topK=4):
        if type(userInput) is str:
            userInput = [userInput]

        inputEmbedding = self.embeddingModel.encode(userInput)
        crossProduct, indexArray = self.documentVectorStore.search(inputEmbedding, k=topK)

        ans = []
        for indexList in indexArray:
            ans.append([])
            for i in indexList:
                ans[-1].append(self.documentContent[i])

        return ans

    def retrieveExample(self, userInput, topK=4, exampleType="Model"):
        if type(userInput) is str:
            userInput = [userInput]

        inputEmbedding = self.embeddingModel.encode(userInput)
        crossProduct, indexArray = self.fewshotVectorStore.search(inputEmbedding, k=topK)

        ans = []
        for indexList in indexArray:
            ans.append([])
            for i in indexList:
                ans[-1].append(self.fewshotContent[i][exampleType])

        return ans