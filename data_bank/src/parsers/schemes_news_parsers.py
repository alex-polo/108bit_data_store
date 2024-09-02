from typing import List

from .news_parsers import wirenboard_parser

list_news_parsers: List[dict] = [
    {
        'system_name': 'news_wirenboard_parser',
        'parser_name': 'Wirenboard',
        'parser_type': 'news_parser',
        'parser_func': wirenboard_parser
    },
]
