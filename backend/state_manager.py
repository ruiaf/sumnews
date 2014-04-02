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
        self.repository = {}
        for (edition_code, edition_name) in settings.editions:
            self.repository[edition_code] = DocumentRepository()

        self.feeds = FeedManager(self.repository)
        self.state_file = state_file

        if os.path.isfile(self.state_file):
            self.deserialize()

        threading.Thread.__init__(self, *args, **kwargs)

    def run(self):
        self.feeds.start()
        for (edition_code, edition_name) in settings.editions:
            self.repository[edition_code].clustering.start()

        while True:
            self.serialize()
            time.sleep(settings.STATE_SAVER_INTERVAL)

    def run_for_unittest(self):
        for (edition_code, edition_name) in settings.editions:
            self.repository[edition_code].clustering.run_for_unittest()

    def serialize(self):
        logging.info("Serializing to %s", settings.STATE_FILE)
        ts = time.time()
        self.feeds.lock.acquire()
        total_docs = 0
        docs = []
        for (edition_code, edition_name) in settings.editions:
            self.repository[edition_code].lock.acquire()
            docs.append((edition_code, self.repository[edition_code].documents))
            total_docs += len(self.repository[edition_code].documents)

        state = (docs, self.feeds.feeds)
        output_file = open(settings.STATE_FILE, 'wb')
        pickle.dump(state, output_file)
        output_file.close()
        logging.info("Serialized %d feeds and %d docs", len(self.feeds.feeds), total_docs)

        for (edition_code, edition_name) in settings.editions:
            self.repository[edition_code].lock.release()
        self.feeds.lock.release()

        te = time.time()
        logging.info("Serializing locked the state for %2.2f seconds", te - ts)

    def deserialize(self):
        logging.info("Deserializing from %s", self.state_file)
        input_file = open(self.state_file, 'rb')
        (docs, feeds) = pickle.load(input_file)
        logging.info("Deserialized %d feeds and %d editions", len(feeds), len(docs))
        input_file.close()
        for (edition_code, edition_docs) in docs:
            self.repository[edition_code].documents = edition_docs
            self.repository[edition_code].rebuild()
        self.feeds.feeds = feeds