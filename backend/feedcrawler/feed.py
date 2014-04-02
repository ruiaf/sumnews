from datetime import datetime
from urllib import request
from http import client
from xml.etree import ElementTree
import logging
import hashlib

from dateutil import parser as dateparser, tz

from documents.document import Document
from feedcrawler.utils import strip_html


class Feed(object):
    def __init__(self, feed_configuration):
        self.name = feed_configuration["name"]
        self.url = feed_configuration["url"]
        self.editions = feed_configuration["editions"]
        self.last_updated = datetime.min
        self.processed_guids = {}
        self.document_count = 0
        self.timezone = tz.tzutc()
        if "timezone" in feed_configuration:
            self.timezone = feed_configuration["timezone"]
        self.force_timezone = False
        if "force_timezone" in feed_configuration:
            self.force_timezone = feed_configuration["force_timezone"]

    def update(self):
        try:
            response = request.urlopen(self.url)
            logging.info("Crawling %s : Got %s %s", self.url, response.status, response.reason)

            docs = []
            if response.status == client.OK:
                content = response.read()
                root = ElementTree.fromstring(content)
                docs = self.get_docs_from_xml(root)

            self.last_updated = datetime.now()
            return docs
        except Exception as e:
            logging.error("Failed to update %s, exception:", e)
            return []

    def get_docs_from_xml(self, root):
        docs = []
        for channel in root:
            for item in channel.findall("item"):
                new_doc = Document()
                new_doc.title = item.find("title").text or ""

                new_doc.download_date = datetime.now(tz.tzutc())
                new_doc.publish_date = dateparser.parse(item.find("pubDate").text, "") or new_doc.download_date
                if new_doc.publish_date.tzinfo is None or self.force_timezone:
                    new_doc.publish_date=new_doc.publish_date.replace(tzinfo=self.timezone)
                new_doc.publish_date = new_doc.publish_date.astimezone(tz.tzutc())

                new_doc.source_url = item.find("link").text or ""

                new_doc.content = strip_html(item.find("description").text or "")

                if item.find("guid"):
                    new_doc.guid = hashlib.md5(item.find("guid").encode('utf-8')).hexdigest()
                else:
                    new_doc.guid = hashlib.md5(new_doc.content.encode('utf-8')).hexdigest()
                new_doc.provider = self.name

                if new_doc.guid not in self.processed_guids:
                    self.processed_guids[new_doc.guid] = True
                    self.document_count += 1
                    docs.append(new_doc)

        return docs
