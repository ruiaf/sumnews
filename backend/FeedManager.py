from datetime import datetime, timedelta
import time
import threading

class FeedManager(threading.Thread):
    def setup(self, feed_list, document_repository):
        self.feed_list = feed_list
        self.document_repository = document_repository

    def run(self):
        for i in range(10):
            self.document_repository.add([  {'title': 'one piece of news title',
                                               'date': datetime.now() - timedelta(minutes = 10),
                                               'content': 'a piece of news retrieved from the back end'},
                                              {'title': 'second piece of news title',
                                               'date': datetime.now() - timedelta(hours = 50),
                                               'content': 'another piece of news retrieved from the backend'}])
            time.sleep(10)