import hashlib
import json
import os
import re
import time
from urllib.request import urlopen
from urllib.parse import urlparse
import argparse
import webbrowser
import configparser
from datetime import datetime

# third party
from bs4 import BeautifulSoup

# Locals
from src.funct import change_since_last_time, file_path


REGEX_FOR_URL = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

START_PROGRAM_TIME = time.time()

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "output", "changes_db.json")

if __name__ == "__main__":
    # Argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url_list",
        nargs="+",
        default=[],
        help="List of url to analyse. Wrong urls will be ignored.",
    )
    parser.add_argument(
        "-o",
        "--open_url",
        default=False,
        action="store_true",
        help="Boolean, if true it opens the url in your preferred webbrowser",
    )
    parser.add_argument(
        "-f",
        "--file",
        nargs=1,
        type=file_path,
        help="Specifies a path to a file with a list of browsers in it.",
    )
    parser.add_argument(
        "-b",
        "--body_only",
        default=True,
        action="store_false",
        help="Default to True. If used the hashes will be created with the whole page.",
    )
    parser.add_argument(
        "-c",
        "--changed_only",
        default=True,
        action="store_false",
        help="Default to True. Doesn't store the new value if the hashes are identical from the previous ones.",
    )
    parser.add_argument(
        "-d",
        "--dump_traces",
        default=False,
        action="store_true",
        help="Default to False. If used creates a file with the content extracted.",
    )

    args = parser.parse_args()
    urls_from_file = []

    if args.file is not None:
        config = configparser.ConfigParser()
        config.read(args.file[0])
        # we catch the different tags
        tags = config.sections()
        # for now we just extract every url

        for a_tag in config.sections():
            for a_nickname in config[a_tag]:
                urls_from_file.append(config[a_tag][a_nickname])

    urls_combined = set(urls_from_file + args.url_list)
    print(f"{urls_combined = }")

    # validate urls
    valid_urls = [
        an_url
        for an_url in urls_combined
        if all(
            [
                getattr(urlparse(an_url), qualifying_attr)
                for qualifying_attr in ("scheme", "netloc")
            ]
        )
    ]

    valid_urls = [
        an_url[:-1] if an_url.endswith("/") else an_url for an_url in valid_urls
    ]
    print(f"{valid_urls = }")

    # reading the changes DB in order to take them in account if we already
    # scanned the url.
    with open(DB_FILEPATH, "r") as readable:
        changes = json.load(readable)

    for url in valid_urls:
        if url.endswith("/"):
            url = url[:-1]
        # request url
        content = str(urlopen(url=url).read())
        content = BeautifulSoup(content, features="html.parser")
        if args.body_only:
            content = content.body
        content = content.strings
        content = "".join(content).encode("utf-8")
        if args.dump_traces:
            with open(
                os.path.join(
                    os.path.dirname(DB_FILEPATH),
                    f"{datetime.now().strftime('%Y%m%d')}_{urlparse(url).netloc}.txt",
                ),
                "w+",
            ) as trace_file:
                trace_file.writelines(content.decode())
        md5_res = hashlib.md5(content)
        sha256_res = hashlib.sha256(content)
        current_time = time.time()
        # Format inside the JSON: {url->{_time->(md5,sha256)}}
        if url not in changes:
            changes[url] = {}
        elif args.changed_only:
            last_time = list(changes[url].keys())[-1]
            if changes[url][last_time] == {"md5": md5_res.hexdigest(), "sha256": sha256_res.hexdigest(),}:
                continue

        # changes[url].append(current_time)
        changes[url][current_time] = {
            "md5": md5_res.hexdigest(),
            "sha256": sha256_res.hexdigest(),
        }

    # writing the data back in the file
    with open(DB_FILEPATH, "w+") as open_file:
        changes = json.dump(changes, open_file, indent=4)

    changed_urls = change_since_last_time(valid_urls, DB_FILEPATH, START_PROGRAM_TIME)

    print(f"{changed_urls = }")
    if args.open_url:
        for an_url in changed_urls:
            webbrowser.open(an_url, new=1)
