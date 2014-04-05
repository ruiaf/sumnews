
from urllib import request
from http import client
import time
import threading
import logging
import settings as main_settings

class DocumentCrawler(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.lock = threading.Lock()
        self.links_to_add_lock = threading.Lock()
        self.links_to_crawl = []
        self.links_to_add = []
        threading.Thread.__init__(self, *args, **kwargs)

    def run(self):
        while True:
            self.lock.acquire()
            for (link, docs) in self.links_to_crawl:
                self.crawl_link(link, docs)
            self.links_to_add_lock.acquire()
            self.links_to_crawl = self.links_to_add
            self.links_to_add = []
            self.links_to_add_lock.release()
            self.lock.release()
            time.sleep(main_settings.DOCUMENT_CRAWLER_INTERVAL)

    def add(self, link, doc_instances):
        self.links_to_add_lock.acquire()
        self.links_to_add.append((link, doc_instances))
        self.links_to_add_lock.release()

    def crawl_link(self, link, doc_instances):
        try:
            response = request.urlopen(link)
            logging.info("Crawling Document %s : Got %s %s", link, response.status, response.reason)

            if response.status == client.OK:
                content = response.read()
                logging.info(content)
        except Exception as e:
            logging.error("Failed to crawl with exception: %s", e)
