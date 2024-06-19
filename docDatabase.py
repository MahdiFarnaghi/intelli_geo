import requests
from bs4 import BeautifulSoup

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLSectionSplitter

class DocDatabase:
    def __init__(self, vectorDataBase, embedding, version):
        self.vectorDataBase = vectorDataBase
        self.cookbookPrefixURL = f"https://docs.qgis.org/{version}/en/docs/pyqgis_developer_cookbook/"
        self.functionURL = f"https://docs.qgis.org/{version}/en/docs/user_manual/expressions/functions_list.html"
        self.docLink = self.getCookbookLink()
        self.embedding = embedding
        self.vectorStore = self.getVectorStore()

    def getCookbookLink(self) -> list[str]:
        response = requests.get(self.cookbookPrefixURL)
        docLink = []
        # Check if the request was successful
        if response.status_code == 200:
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
                docLink.append(self.cookbookPrefixURL + link)
        else:
            raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        return docLink

    def getQgsFunctionDoc(self):
        # Send an HTTP GET request to the URL
        response = requests.get(self.functionURL)

        if response.status_code == 200:
            # Get the HTML content from the response
            htmlContent = response.text
        else:
            raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        headersSplitOn = [
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3"),
            ("h4", "Header 4"),
        ]

        htmlSplitter = HTMLSectionSplitter(headers_to_split_on=headersSplitOn)
        htmlHeaderSplits = htmlSplitter.split_text(htmlContent)

        return htmlHeaderSplits

    def getVectorStore(self):
        loader = WebBaseLoader(self.docLink)
        docs = loader.load()
        docs += self.getQgsFunctionDoc()

        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        vectorStore = self.vectorDataBase.from_documents(documents, self.embedding)

        return vectorStore

    def retrieve(self, userInput):
        retriever = self.vectorStore.as_retriever()
        document = retriever.invoke(userInput)

        return document






