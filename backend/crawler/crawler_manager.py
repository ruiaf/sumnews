"""
Continuously monitors feeds and adds new content to the document_repository
"""

import time
import threading
import logging
from copy import copy

from crawler import settings
import settings as main_settings
from crawler.feed import Feed
from crawler.document_crawler import DocumentCrawler


class CrawlerManager(threading.Thread):
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
        self.document_crawler = DocumentCrawler()
        self.document_crawler.start()
        threading.Thread.__init__(self, *args, **kwargs)

    def run(self):
        """
        Run the feed manager (in its own thread)
        """

        while True:
            # rss feed crawling
            self.lock.acquire()
            for feed in self.feeds:
                documents = feed.update()
                for doc in documents:
                    doc_instances = []
                    for edition in feed.editions:
                        new_doc = copy(doc)
                        self.document_repository[edition].add([new_doc])
                        doc_instances.append(new_doc)
                    self.document_crawler.add(doc.source_url, doc_instances)

            self.lock.release()

            time.sleep(main_settings.FEED_CRAWLER_INTERVAL)