from typing import List

from .schemes_catalogs_parsers import list_catalogs_parsers
from .schemes_news_parsers import list_news_parsers

list_parsers: List[dict] = list()

list_parsers.extend(list_news_parsers)
list_parsers.extend(list_catalogs_parsers)
