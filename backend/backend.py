"""
This is the backend of the news service summarization.
It initialized the following main components:
    DocumentRepository: Responsible for storing the news content and summaries
    FeedManager: Responsible for getting Documents from news Feeds
                 and storing it in the DocumentRepository
    SumNewsService: Responsible for processing requests coming from the coreux
"""

from request_manager import RequestListner
from state_manager import StateManager
import settings



class BackendService(object):
    """
    Manages the backend service
    """

    @staticmethod
    def start():
        """
        Start the Backend service
        """
        state = StateManager(settings.STATE_FILE)
        state.start()
        listner = RequestListner(state.repository)
        listner.start()

if __name__ == "__main__":
    BackendService.start()
