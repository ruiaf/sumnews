from datetime import datetime
from dateutil import tz


class Summary(object):
    def __init__(self):
        self.guid = ""
        self.title = ""
        self.sentences = []
        self.publish_date = datetime.now(tz.tzutc())

    def as_dictionary(self):
        data = {
            'guid': self.guid,
            'title': self.title,
            'sentences': [],
            'publish_date': self.publish_date,
            'debug': {
            }
        }

        for sentence in self.sentences:
            data['sentences'].append(sentence.text)

        return data