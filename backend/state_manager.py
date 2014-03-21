import threading
import time
import pickle
import logging
import os.path

import settings
from feedcrawler.feed_manager import FeedManager
from documents.document_repository import DocumentRepository


class StateManager(threading.Thread):
    def __init__(self, state_file, *args, **kwargs):
        self.repository = DocumentRepository()
        self.feeds = FeedManager(self.repository)
        self.state_file = state_file

        if os.path.isfile(self.state_file):
            self.deserialize()

        threading.Thread.__init__(self, *args, **kwargs)

    def get_state(self):
        return self.repository, self.feeds

    def run(self):
        self.feeds.start()
        self.repository.clustering.start()
        while True:
            self.serialize()
            time.sleep(settings.STATE_SAVER_INTERVAL)

    def run_for_unittest(self):
        self.repository.clustering.run_for_unittest()

    def serialize(self):
        logging.info("Serializing to %s", settings.STATE_FILE)
        self.feeds.lock.acquire()
        ts = time.time()
        self.repository.lock.acquire()
        state = (self.repository.documents, self.feeds.feeds)
        output_file = open(settings.STATE_FILE, 'wb')
        pickle.dump(state, output_file)
        output_file.close()
        logging.info("Serialized %d feeds and %d docs", len(self.feeds.feeds), len(self.repository.documents))
        self.feeds.lock.release()
        self.repository.lock.release()
        te = time.time()
        logging.info("Serializing locked the state for %2.2f seconds", te - ts)

    def deserialize(self):
        logging.info("Deserializing from %s", self.state_file)
        input_file = open(self.state_file, 'rb')
        (docs, feeds) = pickle.load(input_file)
        logging.info("Deserialized %d feeds and %d docs", len(feeds), len(docs))
        input_file.close()
        self.repository.documents = docs
        self.repository.rebuild()
        self.feeds.feeds = feeds