from dateutil import tz

FEEDS = [
    {
        "name": "CNN",
        "url": "http://rss.cnn.com/rss/edition.rss",
    },
    {
        "name": "BBC",
        "url": "http://feeds.bbci.co.uk/news/rss.xml",
    },
    {
        "name": "Reuters",
        "url": "http://feeds.reuters.com/reuters/topNews",
    },
    {
        "name": "Independent",
        "url": "http://www.independent.co.uk/?service=Rss",
    },
    {
        "name": "NPR",
        "url": "http://www.npr.org/rss/rss.php?id=1001",
    },
    {
        "name": "NY Times",
        "url": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    },
    {
        "name": "Sky News",
        "url": "http://news.sky.com/feeds/rss/home.xml",
    },
    {
        "name": "US News",
        "url": "http://www.usnews.com/rss/news",
    },
    {
        "name": "Wall Street Journal",
        "url": "http://online.wsj.com/xml/rss/3_7011.xml",
        "timezone": tz.tzoffset("EST", -4*60*60),
        "force_timezone": True
    },
    {
        "name": "Washington Post",
        "url": "http://feeds.washingtonpost.com/rss/homepage",
    },
    {
        "name": "CBS News",
        "url": "http://www.cbsnews.com/latest/rss/main",
        "timezone": tz.tzutc(),
        "force_timezone": True
    }
]
