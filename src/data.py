from dataclasses import dataclass


@dataclass
class ChangedWebsite:
    nickname: str  # name
    time: str  # date in format YYYYMMDD
    url: str  # url to the site
    tag: str  # optional tag?
