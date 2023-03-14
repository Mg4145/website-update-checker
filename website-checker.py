import hashlib
import json
import os
import re
import time
from urllib.request import urlopen
from urllib.parse import urlparse


REGEX_FOR_URL = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

if __name__ == "__main__":
    url_valid = False
    while url_valid is False:
        url = input("Valid url to analyse :")
        tokens = urlparse(url)
        url_valid = all([getattr(tokens, qualifying_attr)
                for qualifying_attr in ('scheme', 'netloc')])

    # reading the changes DB in order to take them in account if we already scanned the url.
    with open(os.path.join(os.path.dirname(__file__), "output", "changes_db.json"), "r") as readable:
        changes = json.load(readable)


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
    with open(os.path.join(os.path.dirname(__file__), "output", "changes_db.json"), "w+") as open_file:
        changes = json.dump(changes, open_file, indent=4)
