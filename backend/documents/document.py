"""
Represents and manages a news document
"""

from datetime import datetime
from dateutil import tz
import re
from crawler import utils


class Document(object):
    """
    News document and its properties
    """

    def __init__(self):
        self.guid = None
        self.title = ""
        self.content = ""
        self.original_summary = ""
        self.provider = ""
        self.tags = []
        self.author = ""
        self.source_url = ""
        self.publish_date = datetime.now(tz.tzutc())
        self.download_date = datetime.now(tz.tzutc())
        self._words = None
        self.exemplar = self
        self.children = []
        self.responsibility_parent = None
        self.availability_parent = None
        self.similarity_parent = None
        self._sentences = None

    def __lt__(self, other):
        return self.publish_date < other.publish_date

    def sentences(self):
        tmp_sentences = [Sentence(utils.strip_html(self.title))]
        tmp_sentences.extend([Sentence(utils.strip_html(s)) for s in self.original_summary.split('[.]') if len(s.strip()) > 0])
        tmp_sentences.extend([Sentence(utils.strip_html(s)) for s in self.content.split('[.]') if len(s.strip()) > 0])
        return tmp_sentences

    def words(self):
            if self._words is None:
                self._words = set(w.lower().strip() for w in re.findall(r"[\w]+", self.content))
                self._words |= set(w.lower().strip() for w in re.findall(r"[\w]+", self.title))
                self._words |= set(w.lower().strip() for w in re.findall(r"[\w]+", self.original_summary))
            return self._words

    def as_dictionary(self):
        data = {
            'guid': self.guid,
            'title': self.title,
            'content': self.content,
            'original_summary': self.original_summary,
            'provider': self.provider,
            'tags': self.tags,
            'author': self.author,
            'source_url': self.source_url,
            'publish_date': self.publish_date,
            'debug': {
                'how well-suited is parent among potential exemplars (responsibility)': self.responsibility_parent,
                'how appropriate is parent according to others (availability)': self.availability_parent,
                'similarity to parent': self.similarity_parent,
            }
        }

        return data


class Sentence(object):
    def __init__(self, text):
        self.text = text
        self._words = None
        self.exemplar = self
        self.children = []
        self.responsibility_parent = None
        self.availability_parent = None
        self.similarity_parent = None

    def words(self):
            if self._words is None:
                self._words = set(w.lower().strip() for w in re.findall(r"[\w]+", self.text))
            return self._words

    def __lt__(self, other):
        return True