import hashlib
import json
import os
import re
import time
from urllib.request import urlopen
from urllib.parse import urlparse
import argparse
import webbrowser

from src.funct import change_since_last_time


REGEX_FOR_URL = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

START_PROGRAM_TIME = time.time()

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "output", "changes_db.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs='+', help="List of url to analyse. Wrong urls will be ignored.")
    parser.add_argument("-o","--open_url", default=False, action="store_true", help="List of url to analyse. Wrong urls will be ignored.")
    args = parser.parse_args()
    print(args)
    valid_urls = [an_url for an_url in args.url if all([getattr(urlparse(an_url), qualifying_attr) for qualifying_attr in ('scheme', 'netloc')])]

    print(f"Kept valid urls : {valid_urls}")
    # reading the changes DB in order to take them in account if we already scanned the url.
    with open(DB_FILEPATH, "r") as readable:
        changes = json.load(readable)

    for url in valid_urls:
        if url.endswith("/"):
            url = url[:-1]
        # request url
        content = urlopen(url=url).read()

        md5_res = hashlib.md5(content)
        sha256_res = hashlib.sha256(content)
        current_time = time.time()
        # so the format inside the json is {url->{_time->(md5,sha256)}}
        if url not in changes:
            changes[url] = {}

        #changes[url].append(current_time)
        changes[url][current_time] = {"md5": md5_res.hexdigest(), "sha256": sha256_res.hexdigest()}

    # writing the data back in the file
    with open(DB_FILEPATH, "w+") as open_file:
        changes = json.dump(changes, open_file, indent=4)

    changed_url = change_since_last_time(urls=valid_urls, db_file_path=DB_FILEPATH, start_time=START_PROGRAM_TIME)

    print(f"changed url since last time : {changed_url}")
    if args.open_url:
        for an_url in changed_url:
            webbrowser.open(an_url, new=1)
