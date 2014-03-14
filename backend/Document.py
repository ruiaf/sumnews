"""
Represents and manages a news document
"""

from datetime import datetime
from dateutil import tz


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

    def __lt__(self, other):
        return self.publish_date < other.publish_date