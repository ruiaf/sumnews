import logging
import threading
import time
import settings
import utils


class ClusterMaker(threading.Thread):
    def __init__(self, document_repository, *args, **kwargs):
        self.document_repository = document_repository
        self.comparator = DocComparator(self.document_repository.index)
        self.documents = []
        self.responsibility = {}
        self.availability = {}
        self.exemplars = {}
        self.lock = threading.Lock()
        self.add_list = []
        self.add_list_lock = threading.Lock()
        threading.Thread.__init__(self, *args, **kwargs)

    def add(self, doc):
        self.add_list_lock.acquire()
        self.add_list.append(doc)
        self.add_list_lock.release()

    def _process_add_list(self):
        self.add_list_lock.acquire()
        self.lock.acquire()

        for doc in self.add_list:
            self.documents.append(doc)
            self.responsibility[len(self.documents) - 1] = {}
            self.availability[len(self.documents) - 1] = {}

        self.add_list = []
        self.add_list_lock.release()
        self.lock.release()

    def clear(self):
        logging.info("Clearing clusters")
        self.lock.acquire()
        self.add_list_lock.acquire()
        self.comparator = DocComparator(self.document_repository.index)
        self.documents = []
        self.responsibility = {}
        self.availability = {}
        self.exemplars = {}
        self.add_list = []
        self.lock.release()
        self.add_list_lock.release()

    def run(self):
        while True:
            ts = time.time()
            self._iterate_affinity()
            te = time.time()

            logging.info("Finished affinity iteration for: %d documents in %2.2f seconds", len(self.documents), te - ts)

            self._process_add_list()
            time.sleep(settings.CLUSTERING_INTERVAL)

    def run_for_unittest(self):
        for i in range(10):
            ts = time.time()
            self._iterate_affinity()
            te = time.time()
            logging.info("Finished affinity iteration for: %d documents in %2.2f seconds", len(self.documents), te - ts)
            self._process_add_list()

    def _iterate_affinity(self):
        self.lock.acquire()
        for i in range(len(self.documents)):
            values = utils.max2((self.availability[i].get(k_prime, 0.0) +
                                self.comparator.similarity(self.documents[i], self.documents[k_prime]),
                                k_prime) for k_prime in range(len(self.documents)))

            self.exemplars[self.documents[i]] = self.documents[values[0][1]]

            for k in range(len(self.documents)):
                sim = self.comparator.similarity(self.documents[i], self.documents[k])
                max_value = next(x[0] for x in values if x[1] != k)
                self.responsibility[i][k] = settings.CLUSTERING_DUMPING_FACTOR * self.responsibility[i].get(k, 0.0) +\
                                            (1 - settings.CLUSTERING_DUMPING_FACTOR) * (sim - max_value)

        for k in range(len(self.documents)):
            sum_value = 0.0
            for i_prime in range(len(self.documents)):
                sum_value += max(0.0, self.responsibility[i_prime].get(k, 0.0))

            for i in range(len(self.documents)):
                self.availability[i][k] = settings.CLUSTERING_DUMPING_FACTOR * self.availability[i].get(k, 0.0) + \
                                          (1 - settings.CLUSTERING_DUMPING_FACTOR) * min(0.0, self.responsibility[k].get(k, 0.0) +
                                                                                         sum_value -
                                                                                         max(0.0, self.responsibility[i].get(k, 0.0)) -
                                                                                         max(0.0, self.responsibility[k].get(k, 0.0)))

            self.availability[k][k] = settings.CLUSTERING_DUMPING_FACTOR * self.availability[k].get(k, 0.0) +\
                                      (1 - settings.CLUSTERING_DUMPING_FACTOR) * (sum_value - max(0.0, self.responsibility[k].get(k, 0.0)))

        self.lock.release()

    def debug(self, doc):
        doc_index = self.documents.index(doc)
        exemplar_index = self.documents.index(self.exemplars[doc])
        print("----------------------------------------------------------------------------------------------------")
        print("Document: %s" % doc.title)
        print("Exemplar: %s" % self.exemplars[doc].title)
        print("Self-Availability %2.2f" % self.availability[doc_index][doc_index])
        print("Self-Responsibility %2.2f" % self.responsibility[doc_index][doc_index])
        if doc_index != exemplar_index:
            print("Document-Exemplar similarity %2.2f" % self.comparator.similarity(doc, self.exemplars[doc]))
            print("Exemplar-Availability %2.2f" % self.availability[doc_index][exemplar_index])
            print("Exemplar-Responsibility %2.2f" % self.responsibility[doc_index][exemplar_index])


class DocComparator(object):
    def __init__(self, inverted_index):
        self.index = inverted_index
        self.cache = {}

    def similarity(self, doc1, doc2):
        if doc1 is doc2:
            return settings.CLUSTERING_DEFAULT_PREFERENCE

        if (doc1, doc2) not in self.cache:
            intersection_words = doc1.words() & doc2.words()
            other_words = doc1.words() ^ doc2.words()
            intersection_word_weight = sum(self.index.tf_idf(word) for word in intersection_words)
            other_words_weight = sum(self.index.tf_idf(word) for word in other_words)
            self.cache[(doc1, doc2)] = intersection_word_weight / (intersection_word_weight + other_words_weight + 0.01)
            self.cache[(doc2, doc1)] = self.cache[(doc1, doc2)]
        return self.cache[(doc1, doc2)]
