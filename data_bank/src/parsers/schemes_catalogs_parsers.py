from typing import List

from src.parsers import catalog_parsers

list_catalogs_parsers: List[dict] = [
    {
        'system_name': 'catalog_bolid_parser',
        'parser_name': 'bolid_scheme',
        'parser_type': 'catalog_parser',
        'parser_func': catalog_parsers.bolid
    },
    # {
    #     'system_name': 'wirenboard_parser_1',
    #     'parser_name': 'Wirenboard2',
    #     'parser_type': 'news_parser',
    #     'parser_func': wirenboard_parser
    # },
]


