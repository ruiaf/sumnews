"""
Represents and manages a news document
"""

from datetime import datetime


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
        self.publish_date = datetime.now()
        self.download_date = datetime.now()
