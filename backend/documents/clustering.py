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

        ts = time.time()
        for doc in self.add_list:
            self.documents.append(doc)
            self.responsibility[doc] = {}
            self.availability[doc] = {}
            self.responsibility[doc][doc] = 0.0
            self.availability[doc][doc] = 0.0
            for other_doc in self.documents:
                if self.comparator.similarity(doc, other_doc) >= settings.CLUSTERING_MINIMUM_SIMILARITY:
                    self.responsibility[doc][other_doc] = 0.0
                    self.availability[doc][other_doc] = 0.0
                    self.responsibility[other_doc][doc] = 0.0
                    self.availability[other_doc][doc] = 0.0

        te = time.time()
        if len(self.add_list):
            logging.info("Finished adding %d documents to clustering in %2.2f seconds", len(self.add_list), te - ts)

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
        for i in self.documents:
            values = utils.max2((self.availability[i][k_prime] + self.comparator.similarity(i, k_prime),
                                k_prime) for k_prime in self.responsibility[i].keys())

            for k in self.responsibility[i].keys():
                sim = self.comparator.similarity(i, k)

                max_value = values[0][0]
                if values[0][1] is k:
                    if len(values) > 2: max_value = values[1][0]
                    else: max_value = 0.0

                self.responsibility[i][k] = ((settings.CLUSTERING_DUMPING_FACTOR * self.responsibility[i][k]) +
                                             (1 - settings.CLUSTERING_DUMPING_FACTOR) * (sim - max_value))

        for k in self.documents:
            sum_value = 0.0
            for i_prime in self.responsibility[k].keys():
                sum_value += max(0.0, self.responsibility[i_prime][k])

            for i in self.responsibility[k].keys():
                self.availability[i][k] = (settings.CLUSTERING_DUMPING_FACTOR * self.availability[i][k] +
                                           (1 - settings.CLUSTERING_DUMPING_FACTOR) *
                                           min(0.0, (self.responsibility[k][k] +
                                                     sum_value -
                                                     max(0.0, self.responsibility[i][k]) -
                                                     max(0.0, self.responsibility[k][k]))))

            self.availability[k][k] = ((settings.CLUSTERING_DUMPING_FACTOR *
                                        self.availability[k][k]) +
                                       ((1 - settings.CLUSTERING_DUMPING_FACTOR) *
                                        (sum_value - max(0.0, self.responsibility[k][k]))))

        for i in self.documents:
            if not i.exemplar is i and i in i.exemplar.children:
                i.exemplar.children.remove(i)

            exemplar = max((self.availability[i][k_prime] + self.responsibility[i][k_prime], k_prime)
                           for k_prime in self.availability[i].keys())

            i.exemplar = exemplar[1]
            i.responsibility_parent = self.responsibility[i][exemplar[1]]
            i.availability_parent = self.availability[i][exemplar[1]]
            i.similarity_parent = self.comparator.similarity(i, exemplar[1])
            if not i.exemplar is i:
                i.exemplar.children.append(i)

        self.lock.release()

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
            sim = intersection_word_weight / (intersection_word_weight + other_words_weight + 0.01)

            if sim >= settings.CLUSTERING_MINIMUM_SIMILARITY:
                self.cache[(doc1, doc2)] = sim
                self.cache[(doc2, doc1)] = sim

            return sim

        return self.cache[(doc1, doc2)]
