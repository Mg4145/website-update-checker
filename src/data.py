from dataclasses import dataclass

@dataclass
class ChangedWebsite:
    name : str  # domain name
    time : str  # date in format YYYYMMDD
    url : str  # url to the site