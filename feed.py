import os
from datetime import UTC, datetime

import feedparser
from feedgen.feed import FeedGenerator
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


def main(urls: list, file: str, title: str, link: str, desc: str):
    feed = Feed(title, link, desc)
    feed.load_file(file)
    for u in urls:
        t = retrieve_title(u)
        feed.append_item(t, u)
    feed.write_file(file)
    return f'Added {u} as "{t}" to {file}'


def retrieve_title(url: str) -> str:
    try:
        with YoutubeDL() as ydl:
            if info := ydl.extract_info(url, download=False):
                title = info.get("title", url)
            else:
                title = url
    except DownloadError:
        title = url
    return title


class Feed:
    def __init__(self, title, link, desc):
        self.build_date = datetime.now(UTC)
        fg = FeedGenerator()
        fg.title(title)
        fg.description(desc)
        fg.link(href=link, rel="alternate")
        self.feed = fg

    def load_file(self, file):
        if os.path.isfile(file):
            for entry in feedparser.parse(file).entries:
                fe = self.feed.add_entry()
                fe.title(entry.title)
                fe.link(href=entry.link)
                if hasattr(entry, "published"):
                    fe.pubDate(entry.published)
                if hasattr(entry, "guid"):
                    fe.guid(entry.guid)

    def write_file(self, file):
        if basedir := os.path.dirname(file):
            os.makedirs(basedir, exist_ok=True)
        rss_feed = self.feed.rss_str(pretty=True)
        with open(file, "wb") as f:
            f.write(rss_feed)

    def append_item(self, title: str, url: str):
        url = url.strip()
        fe = self.feed.add_entry()
        fe.link(href=url)
        fe.guid(url, permalink=True)
        fe.title(title)
        fe.pubDate(self.build_date)
