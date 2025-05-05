import argparse
import os
import pathlib
from urllib.parse import urlparse

from feed import main

if __name__ == "__main__":

    def url_type(url):
        parts = urlparse(url)
        if not parts.scheme:
            msg = f"invalid URL: {url!r}"
            raise argparse.ArgumentTypeError(msg)
        return url

    data_dir = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    default_title = "Watch Later Queue"
    default_desc = default_title
    default_file = data_dir + "/watchlater/watch_later.xml"
    default_link = "file://" + default_file

    parser = argparse.ArgumentParser(
        description="Tool to queue up videos/articles as an RSS feed"
    )
    parser.add_argument("url", nargs="+", type=url_type, help="URL to video/article")
    parser.add_argument(
        "-f",
        "--file",
        type=pathlib.Path,
        default=default_file,
        help="path to RSS file, default: %(default)s",
    )
    parser.add_argument(
        "-l",
        "--link",
        type=str,
        default=default_link,
        help="Feed link, default: %(default)s",
    )
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        default=default_desc,
        help='Feed description, default: "%(default)s"',
    )
    parser.add_argument(
        "-t",
        "--title",
        type=str,
        default=default_title,
        help='Feed title, default: "%(default)s"',
    )

    args = parser.parse_args()
    main(args.url, args.file, args.title, args.link, args.description)
