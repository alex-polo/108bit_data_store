# System environment
system_name_news_bot: str = 'news_bot'
system_name_instruktor_bot: str = 'instruktor_bot'
news_bot_min_time: str = 'news_bot_min_time'
news_bot_max_time: str = 'news_bot_max_time'
queue_posts_status_send: str = 'send'
queue_posts_status_archive: str = 'archive'
system_catalog_parser_type: str = 'catalog_parser'
system_news_parser_type: str = 'news_parser'

# Celery settings
config_directory: str = 'config'
celery_logging_config: str = 'config/celery_logging.ini'
scheduler_time: int = 1

# Loader settings
win_webdriver_path: str = 'drivers\\chrome_127.0.6533.99(r1313161)\\chromedriver-win64\\chromedriver.exe'
linux_webdriver_path: str = 'drivers/chrome_127.0.6533.99(r1313161)/chromedriver-linux64/chromedriver'
webdriver_port: int = 8888
webdriver_timeout: int = 5
chrome_page_load_strategy: str = 'normal'
chrome_options: list = ["--enable-automation",
                        "--no-sandbox",
                        "--disable-gpu",
                        "--window-size=1920,1080",
                        "--headless=new"]
