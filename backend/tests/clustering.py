import unittest
import time
import logging
from documents.document import Document
from state_manager import StateManager


class TestClustering(unittest.TestCase):
    def setUp(self):
        self.state = StateManager("database/unittest.pickle")

    def test_clustering_pref(self):
        ts = time.time()
        self.state.run_for_unittest()
        te = time.time()
        logging.info("Clustering perf test took: %2.2f seconds", te - ts)
        self.assertLess(te - ts, 30.0, "Clustering is running slowly")

    def test_tf_idf_perf(self):
        ts = time.time()
        for i in range(100000):
            self.state.repository.index.tf_idf("portugal")
            self.state.repository.index.tf_idf("london")
            self.state.repository.index.tf_idf("ukraine")
            self.state.repository.index.tf_idf("russia")
        te = time.time()
        logging.info("tf_idf perf test took: %2.2f seconds", te - ts)
        self.assertLess(te - ts, 1.0, "tf_idf is running slowly")


class TestSimilarityDistance(unittest.TestCase):
    def setUp(self):
        self.state = StateManager("database/unittest_big.pickle")
        #self.state.run_for_unittest()

    def test_equal_docs(self):
        doc1 = Document()
        doc2 = Document()
        doc1.title = "russia invades ukraine"
        doc1.content = "russia invades ukraine"
        doc2.title = "russia invades ukraine"
        doc2.content = "russia invades ukraine"
        distance = self.state.repository.clustering.comparator.similarity(doc1, doc2)
        logging.info("Similarity is %2.2f", distance)
        self.assertGreater(distance, 0.9)

    def test_very_similar_docs(self):
        doc1 = Document()
        doc2 = Document()
        doc1.title = "russia invades ukraine"
        doc1.content = "russia invades ukraine"
        doc2.title = "russia invaded by ukraine"
        doc2.content = "russia invaded ukraine"
        distance = self.state.repository.clustering.comparator.similarity(doc1, doc2)
        logging.info("Similarity is %2.2f", distance)
        self.assertGreater(distance, 0.3)

    def test_very_different_docs(self):
        doc1 = Document()
        doc2 = Document()
        doc1.title = "russia invades ukraine"
        doc1.content = "russia is invading ukraine again"
        doc2.title = "portugal is cool"
        doc2.content = "portugal is very very cool"
        distance = self.state.repository.clustering.comparator.similarity(doc1, doc2)
        logging.info("Similarity is %2.2f", distance)
        logging.info("tf_idf of \"is\": %2.5f", self.state.repository.index.tf_idf("is"))
        logging.info("tf_idf of \"portugal\": %2.5f", self.state.repository.index.tf_idf("portugal"))
        logging.info("tf_idf of \"ukraine\": %2.5f", self.state.repository.index.tf_idf("ukraine"))
        self.assertLess(distance, 0.05)

    def test_somewhat_different_docs(self):
        doc1 = Document()
        doc2 = Document()
        doc1.title = "russia bought cars in portugal"
        doc1.content = "russia went to portugal and bought 5 new cars"
        doc2.title = "portugal is cool"
        doc2.content = "portugal is very very cool"
        distance = self.state.repository.clustering.comparator.similarity(doc1, doc2)
        logging.info("Similarity is %2.2f", distance)
        logging.info("tf_idf of \"is\": %2.5f", self.state.repository.index.tf_idf("is"))
        logging.info("tf_idf of \"portugal\": %2.5f", self.state.repository.index.tf_idf("portugal"))
        logging.info("tf_idf of \"russia\": %2.5f", self.state.repository.index.tf_idf("russia"))
        self.assertLess(distance, 0.15)

if __name__ == '__main__':
    unittest.main()