from .news_parsers import wirenboard_parser

list_parsers = [
    {
        'system_name': 'wirenboard_parser',
        'parser_name': 'Wirenboard',
        'parser_type': 'news_parser',
        'parser_func': wirenboard_parser
    },
    {
        'system_name': 'wirenboard_parser_1',
        'parser_name': 'Wirenboard2',
        'parser_type': 'news_parser',
        'parser_func': wirenboard_parser
    }
]
