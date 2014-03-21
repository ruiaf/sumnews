import re
import functools


class InvertedIndex(object):
    def __init__(self):
        self.postings = {}
        self.n_documents = 0
        self.n_words = 0

    def add(self, doc):
        self.n_documents += 1
        text_sources = [doc.title, doc.content]
        for text in text_sources:
            for w in re.findall(r"[\w]+", text):
                word = w.lower().strip()
                word_posting = self.postings.get(word, set())
                if doc not in word_posting:
                    word_posting.add(doc)
                    self.n_words +=1
                self.postings[word] = word_posting

    def search(self, keywords, count):
        keywords = [w.lower().strip() for w in keywords]
        matching_postings = [self.postings[keyword] for keyword in keywords if keyword in self.postings]
        if len(matching_postings) == 0:
            return []
        matching_documents = functools.reduce(lambda x, y: x & y, matching_postings)
        return sorted(matching_documents, reverse=True)[:count]

    def clear(self):
        self.postings.clear()

    def tf_idf(self, word):
        val = 1-float(len(self.postings.get(word, []))) / self.n_documents
        return val**8