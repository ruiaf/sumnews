"""
Store for news documents
"""

import threading


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
        Retrieve the @count recent documents
        """
        count = min(count, len(self.documents))
        self.lock.acquire()
        recent_docs = self.documents[:count]
        self.lock.release()
        return recent_docs
