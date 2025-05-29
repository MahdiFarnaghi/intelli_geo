"""
/***************************************************************************

RetrievalVectorbase

This module defines the RetrievalVectorbase class, which manages vector
stores for document retrieval and few-shot learning examples. It leverages
FAISS for efficient vector storage and search, and SentenceTransformer for
encoding text into embeddings.

Classes:
    RetrievalVectorbase: Handles the creation, loading, and querying of
                         vector stores for both documents and few-shot
                         examples.

Usage:
    - Initialize the RetrievalVectorbase with a specified version.
    - Use createDocumentStore and createFewshotStore to set up the vector
      stores.
    - Retrieve relevant documents or examples based on user input using
      retrieveDocument and retrieveExample methods.

Dependencies:
    - requests
    - faiss
    - re
    - os
    - json
    - csv
    - BeautifulSoup from bs4
    - SentenceTransformer from sentence_transformers
    - WebBaseLoader from langchain_community.document_loaders
    - RecursiveCharacterTextSplitter, HTMLSectionSplitter from
      langchain_text_splitters
    - utils (local module)

Note:
    The vector stores are saved in the user's Documents folder under
    "QGIS_IntelliGeo/.vectorDB".
***************************************************************************/
"""

import requests


from .utils import splitAtPattern, show_variable_popup
# from .utils import readURL

class RetrievalVectorbase:
    def __init__(self, version):
        self.version = version
        self.backendURL = "https://owsgip.itc.utwente.nl/intelligeo/"

    def retrieveDocument(self, userInput, topK=4):
        url = self.backendURL + "/retrieve_document/"
        payload = {
            "version": str(self.version),
            "query": str(userInput),
            "topK": topK
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return data["results"]
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return [[]]

    def retrieveExample(self, userInput, topK=4, exampleType="Model"):
        url = self.backendURL + "/retrieve_example/"
        payload = {
            "version": self.version,
            "query": userInput,
            "topK": topK,
            "exampleType": exampleType
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return data["results"]
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return [[]]