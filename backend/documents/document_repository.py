"""
Store for news documents
"""

import threading
import heapq
import logging
import re
from datastructures.inverted_index import InvertedIndex
from documents.clustering import ClusterMaker


class DocumentRepository(object):
    """
    Store for news documents
    """

    def __init__(self):
        self.documents = []
        self.index = InvertedIndex()
        self.clustering = ClusterMaker(self)
        self.lock = threading.Lock()

    def add(self, document_list):
        """
        Add a list of documents to the repository
        """
        self.lock.acquire()
        for doc in document_list:
            heapq.heappush(self.documents, doc)
            self.index.add(doc)
            self.clustering.add(doc)
        self.lock.release()

    def recent_documents(self, count=10):
        """
        Retrieve the count most recent documents
        """
        recent_docs = heapq.nlargest(count, self.documents)
        return recent_docs

    def recent_clusters(self, count=30):
        """
        Retrieve the count most recent documents
        """
        recent_docs = heapq.nlargest(count*10, self.documents)
        clusters = {}
        for doc in recent_docs:
            if doc.exemplar:
                representative = doc.exemplar
            else:
                representative = doc
            cluster = clusters.get(representative, [])
            cluster.append(doc)
            clusters[representative] = cluster

        clusters = [(len(value), value) for value in clusters.values()]
        clusters.sort(reverse=True)
        clusters = clusters[:count]
        return [value for (x, value) in clusters]

    def search(self, query, count=10):
        """
        Retrieve count documents matching the query
        """
        keywords = list(re.findall(r"[\w']+", query))
        results = self.index.search(keywords, count)
        return results

    def search_clusters(self, query, count=10):
        """
        Retrieve count clusters matching the query
        """
        keywords = list(re.findall(r"[\w']+", query))
        retrieved_docs = self.index.search(keywords, count)
        clusters = {}
        for doc in retrieved_docs:
            if doc.exemplar:
                representative = doc.exemplar
            else:
                representative = doc
            cluster = clusters.get(representative, [])
            cluster.append(doc)
            clusters[representative] = cluster

        clusters = [(len(value), value) for value in clusters.values()]
        clusters.sort(reverse=True)
        clusters = clusters[:count]
        return [value for (x, value) in clusters]

    def search_guid(self, guid):
        """
        Retrieve count clusters matching the query
        """

        return self.index.get(guid)

    def rebuild(self):
        logging.info("Rebuilding index")
        self.index.clear()
        self.clustering.clear()
        for doc in self.documents:
            doc.exemplar = doc
            doc.children = []
            self.index.add(doc)
            self.clustering.add(doc)

    def stats(self):
        stats = {
            "Number of indexed documents": self.index.n_documents,
            "Number of indexed words": self.index.n_words,
            "Number of clustered documents": len(self.clustering.documents)
        }

        return stats

