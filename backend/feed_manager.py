"""
Continuously monitors feeds and adds new content to the document_repository
"""
from datetime import datetime, timedelta
import time
import threading


class FeedManager(threading.Thread):
    """
    Continuously monitors feeds and adds new content to the document_repository
    """
    def __init__(self, feed_list, document_repository, *args, **kwargs):
        self.feed_list = feed_list
        self.document_repository = document_repository
        threading.Thread.__init__(self, *args, **kwargs)

    def run(self):
        """
        Run the feed manager ( in its own thread)
        """
        while True:
            self.document_repository.add([
                {'title': 'one piece of news title',
                 'date': datetime.now() - timedelta(minutes=10),
                 'content': 'a piece of news retrieved from the back end'},
                {'title': 'second piece of news title',
                 'date': datetime.now() - timedelta(hours=50),
                 'content': 'another piece of news retrieved from the backend'}]
            )
            time.sleep(10)
