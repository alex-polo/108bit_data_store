# Celery settings
config_directory = 'config'
celery_logging_config = 'config/celery_logging.ini'

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
