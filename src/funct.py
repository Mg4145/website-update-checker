import time
import json
import os
import argparse


def file_path(path: str):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_file:{path} is not a valid path")


def change_since_last_time(
    urls: list, db_file_path: str, start_time: time.time()
) -> list:
    website_updated = []
    with open(db_file_path, "r") as open_file:
        changes = json.load(open_file)

    for a_website in changes.keys():
        if a_website not in urls:
            continue
        elif float(list(changes[a_website].keys())[-1]) <= start_time:
            continue
        else:
            website_updated.append(a_website)

    return website_updated
