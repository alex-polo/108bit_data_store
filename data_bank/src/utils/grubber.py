import logging
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.config import BrowserChromeConfig

logger = logging.getLogger(__name__)


def download_page(url: str, config: BrowserChromeConfig) -> str:
    page_source: str = Optional[None]

    service = Service(executable_path=config.driver_path, port=config.port)
    driver = webdriver.Chrome(service=service, options=config.options)

    try:
        driver.get(url=url)
        driver.implicitly_wait(config.timeout)
        page_source = driver.page_source
    except Exception as error:
        logger.error(error)
    finally:
        driver.close()
        driver.quit()

    return page_source
