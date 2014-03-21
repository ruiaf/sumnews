"""
Continuously monitors feeds and adds new content to the document_repository
"""

import time
import threading

from feedcrawler import settings
import settings as main_settings
from feedcrawler.feed import Feed


class FeedManager(threading.Thread):
    """
    Continuously monitors feeds and adds new content to the document_repository
    """
    def __init__(self, document_repository, *args, **kwargs):
        self.feeds = []
        self.lock = threading.Lock()
        self.lock.acquire()
        for x in settings.FEEDS:
            self.feeds.append(Feed(x))
        self.document_repository = document_repository
        self.lock.release()
        threading.Thread.__init__(self, *args, **kwargs)

    def run(self):
        """
        Run the feed manager (in its own thread)
        """

        while True:
            self.lock.acquire()
            for feed in self.feeds:
                documents = feed.update()
                self.document_repository.add(documents)
            self.lock.release()
            time.sleep(main_settings.FEED_CRAWLER_INTERVAL)
