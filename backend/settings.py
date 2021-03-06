"""
Backend Settings
"""

import logging

NEWS_SERVICE_HOST = ""
NEWS_SERVICE_PORT = 8001
PACKET_MAX_SIZE = 20024

STATE_FILE = "database/state.pickle"

STATE_SAVER_INTERVAL = 5*60
FEED_CRAWLER_INTERVAL = 2*60
DOCUMENT_CRAWLER_INTERVAL = 2*60

CLUSTERING_INTERVAL = 10
CLUSTERING_DUMPING_FACTOR = 0.5
CLUSTERING_DEFAULT_PREFERENCE = 0.10
CLUSTERING_MINIMUM_SIMILARITY = 0.10

logging.root.setLevel(logging.INFO)

editions = [
    ("bg-bg", "Български"),
    ("en-gb", "English - United Kingdom"),
    ("en-us", "English - United States"),
    ("hu-hu", "Magyar"),
    ("pt-pt", "Português - Portugal"),
    ("pt-br", "Português - Brasil"),
    ("uk-uk", "Українська"),
]