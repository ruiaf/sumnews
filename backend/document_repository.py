"""
Store for news documents
"""

import threading
import itertools


class DocumentRepository(object):
    """
    Store for news documents
    """

    def __init__(self):
        self.documents = []
        self.lock = threading.Lock()

    def add(self, document_list):
        """
        Add a list of documents to the repository
        """
        self.lock.acquire()
        self.documents.extend(document_list)
        self.lock.release()

    def recent_documents(self, count=10):
        """
        Retrieve the count most recent documents
        """
        count = min(count, len(self.documents))
        self.lock.acquire()
        recent_docs = self.documents[:count]
        self.lock.release()
        return recent_docs

    def search(self, query, count=10):
        """
        Retrieve count documents matching the query
        """
        self.lock.acquire()
        results = list(itertools.islice(self.__findall(query), count))
        self.lock.release()
        return results

    def __findall(self, query):
        for doc in self.documents:
            if query in doc["title"] or query in doc["content"]:
                yield doc
