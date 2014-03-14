"""
Continuously monitors feeds and adds new content to the document_repository
"""

import time
import threading

from feedcrawler import settings
from feedcrawler.feed import Feed


from document import Document

class FeedManager(threading.Thread):
    """
    Continuously monitors feeds and adds new content to the document_repository
    """
    def __init__(self, document_repository, *args, **kwargs):
        self.feeds = []
        for x in settings.FEEDS:
            self.feeds.append(Feed(x))
        self.document_repository = document_repository
        threading.Thread.__init__(self, *args, **kwargs)

    def run(self):
        """
        Run the feed manager (in its own thread)
        """

        while True:
            for feed in self.feeds:
                documents = feed.update()
                self.document_repository.add(documents)
            time.sleep(5*60)
