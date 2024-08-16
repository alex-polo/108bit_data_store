from .news import wirenboard_parser

parsers = [
    {
        'system_name': 'wirenboard_parser',
        'name': 'Wirenboard',
        'type': 'news_parser',
        'parser': wirenboard_parser,
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
