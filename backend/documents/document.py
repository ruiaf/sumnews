"""
Represents and manages a news document
"""

from datetime import datetime
from dateutil import tz
import re


class Document(object):
    """
    News document and its properties
    """

    def __init__(self):
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

    def __lt__(self, other):
        return self.publish_date < other.publish_date

    def words(self):
            if self._words is None:
                self._words = set(w.lower().strip() for w in re.findall(r"[\w]+", self.content))
                self._words |= set(w.lower().strip() for w in re.findall(r"[\w]+", self.title))
            return self._words
