from .news_parsers import wirenboard_parser

list_parsers = [
    {
        'system_name': 'wirenboard_parser',
        'parser_name': 'Wirenboard',
        'parser_type': 'news_parser',
        'parser_func': wirenboard_parser,
    },
    {
        'system_name': 'wirenboard_parser_1',
        'parser_name': 'Wirenboard2',
        'parser_type': 'news_parser',
        'parser_func': wirenboard_parser,
    }
]

# sites = [
#     {
#         'site_name': 'wirenboard',
#         'is_news_parsing': True,
#         'is_product_parsing': False,
#         'is_enabled': True,
#         'news_parsing': {
#             'url': 'https://wirenboard.com/ru/news/',
#             'vendor': '#Wirenboard',
#             'field_tags': ['#Системы_автоматики', ],
#             'parser': wirenboard_parser
#             # 'image_path_for_news': None,
#         },
#         'product_parsing': {
#             'url': 'https://wirenboard.com',
#             'parser': wirenboard_parser
#         },
#     },
#     {
#         'site_name': 'wirenboard_2',
#         'is_news_parsing': True,
#         'is_product_parsing': False,
#         'is_enabled': True,
#         'news_parsing': {
#             'url': 'https://wirenboard.com/ru/news/',
#             'vendor': '#Wirenboard',
#             'field_tags': ['#Системы_автоматики', ],
#             # 'image_path_for_news': None,
#         },
#         'product_parsing': {
#             'url': 'https://wirenboard.com/ru/news/',
#         },
#     },
# ]
