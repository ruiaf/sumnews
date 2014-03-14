import re


def strip_html(text):
    text = re.sub("<.+?>", "", text)
    text = text.replace("&nbsp;","")
    text = text.replace("Read full article &#62;&#62;","").strip()
    return text
