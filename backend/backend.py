"""
This is the backend of the news service summarization.
It initialized the following main components:
    DocumentRepository: Responsible for storing the news content and summaries
    FeedManager: Responsible for getting Documents from news Feeds
                 and storing it in the DocumentRepository
    SumNewsService: Responsible for processing requests coming from the coreux
"""

from .feed_manager import FeedManager
from .document_repository import DocumentRepository
from .request_manager import RequestListner


class BackendService(object):
    """
    Manages the backend service
    """

    @staticmethod
    def start():
        """
        Start the Backend service
        """
        repository = DocumentRepository()
        feeds = FeedManager([], repository)
        feeds.start()
        listner = RequestListner(repository)
        listner.start()

if __name__ == "__main__":
    BackendService.start()
