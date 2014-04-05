from dateutil import tz

FEEDS = [
    {
        "name": "CNN",
        "url": "http://rss.cnn.com/rss/edition.rss",
        "editions": ["en-us"],
    },
    {
        "name": "BBC",
        "url": "http://feeds.bbci.co.uk/news/rss.xml",
        "editions": ["en-gb"],
    },
    {
        "name": "Reuters",
        "url": "http://feeds.reuters.com/reuters/topNews",
        "editions": ["en-gb", "en-us"],
    },
    {
        "name": "The Independent",
        "url": "http://www.independent.co.uk/?service=Rss",
        "timezone": tz.tzoffset("CET", 4*60*60),
        "force_timezone": True,
        "editions": ["en-gb"],
    },
    {
        "name": "NPR",
        "url": "http://www.npr.org/rss/rss.php?id=1001",
        "editions": ["en-us"],
    },
    {
        "name": "NY Times",
        "url": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "editions": ["en-us"],
    },
    {
        "name": "Sky News",
        "url": "http://news.sky.com/feeds/rss/home.xml",
        "editions": ["en-gb"],
    },
    {
        "name": "US News",
        "url": "http://www.usnews.com/rss/news",
        "editions": ["en-us"],
    },
    {
        "name": "Wall Street Journal",
        "url": "http://online.wsj.com/xml/rss/3_7011.xml",
        "timezone": tz.tzoffset("EST", -4*60*60),
        "force_timezone": True,
        "editions": ["en-us"],
    },
    {
        "name": "Washington Post",
        "url": "http://feeds.washingtonpost.com/rss/homepage",
        "editions": ["en-us"],
    },
    {
        "name": "CBS News",
        "url": "http://www.cbsnews.com/latest/rss/main",
        "timezone": tz.tzutc(),
        "force_timezone": True,
        "editions": ["en-us"],
    },
    {
        "name": "Público",
        "url": "http://feeds.feedburner.com/PublicoRSS?format=xml",
        "editions": ["pt-pt"],
        "timezone": tz.tzoffset("GMT", 1*60*60),
        "force_timezone": True,
    },
    {
        "name": "Jornal de Notícias",
        "url": "http://feeds.jn.pt/JN-ULTIMAS",
        "editions": ["pt-pt"],
        "timezone": tz.tzoffset("GMT", 1*60*60),
        "force_timezone": True,
    },
    {
        "name": "Jornal de Negócios",
        "url": "http://www.jornaldenegocios.pt/funcionalidades/rss/generarRSS.php",
        "editions": ["pt-pt"],
        "timezone": tz.tzoffset("GMT", 1*60*60),
        "force_timezone": True,
    },
    {
        "name": "Diário de Notícias",
        "url": "http://feeds.dn.pt/DN-Ultimas",
        "editions": ["pt-pt"],
        "timezone": tz.tzoffset("GMT", 1*60*60),
        "force_timezone": True,
    },
    {
        "name": "Sábado",
        "url": "http://www.sabado.pt/cmspages/RSSFeeds.aspx",
        "editions": ["pt-pt"],
        "timezone": tz.tzoffset("GMT", 1*60*60),
        "force_timezone": True,
    },
    {
        "name": "Magyar Hírlap",
        "url": "http://www.magyarhirlap.hu/rss.xml",
        "editions": ["hu-hu"],
    },
    {
        "name": "Index",
        "url": "http://index.hu/24ora/rss",
        "editions": ["hu-hu"],
    },
    {
        "name": "Heti Világgazdaság",
        "url": "http://hvg.hu/rss",
        "editions": ["hu-hu"],
    },
    {
        "name": "Metropol",
        "url": "http://www.metropol.hu/rss/cimlap",
        "editions": ["hu-hu"],
    },
    {
        "name": "Népszava",
        "url": "http://www.nepszava.hu/rss/",
        "editions": ["hu-hu"],
    },
    {
        "name": "Világgazdaság",
        "url": "http://www.vg.hu/rss/vg.xml",
        "editions": ["hu-hu"],
    },
]
