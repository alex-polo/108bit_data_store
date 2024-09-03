import re
from datetime import datetime
from typing import List
from urllib.parse import urlparse

import dateparser
from bs4 import BeautifulSoup, element, Tag

from src.config import BrowserChromeConfig
from src.utils import download_page as download
from src.utils.classes import ParsedData, ParserField

# from starting_parameters.misc import download

text_exception_class_style = 'Style classes not found in page html markup'


async def wirenboard_parser(page_body: str,
                            search_time: datetime,
                            browser_config: BrowserChromeConfig,
                            site: dict) -> List[ParsedData]:
    content_class_name = 'article-list__content'
    items_class_name = 'item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    news_list: element.Tag = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items: element.ResultSet = news_list.find_all('div', class_=items_class_name)

    for item in items:
        date = dateparser.parse(item.find('div', class_='date').getText(), settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find("div", class_="name").text
            site_url = site.get("url")[:-9]
            post_link = item.a["href"]

            if site_url in post_link:
                more = post_link
            else:
                more = f'{site_url}{post_link}'
            try:
                image_url = item.find('div', class_='img').find('picture').find('source').get('srcset').split(',')[0][
                            :-3]
            except:
                image_url = None

            details = item.p.text

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def usergate_parser(page_body: str,
                          search_time: datetime,
                          site: dict,
                          request_headers: dict) -> List[ParsedData]:
    items_class_name = 'views-row'
    if items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    news_list = BeautifulSoup(page_body, 'html.parser').find_all('div', class_=items_class_name)

    for item in news_list:
        date = item.find("div", class_="views-field-created").find('span', class_="field-content").text
        date = datetime.strptime(date, "%d.%m.%Y")
        if date >= search_time:
            title_item = item.find("div", class_="views-field-title")
            title = title_item.text
            more = f'{site.get("url")[:-12]}{title_item.a["href"]}'
            details = item.find("span", class_="views-field-body").text

            try:
                response = await download(url=more, headers=request_headers)
                news_content = BeautifulSoup(response.text, 'html.parser').find('div', class_="field-item even")
                image_url = f'{site.get("url")[:-12]}{news_content.find("img")["src"]}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def unitest_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    items_class_name = 'new'
    if items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    news_list = BeautifulSoup(page_body, 'html.parser').find_all("div", class_=items_class_name)

    for item in news_list:
        date = datetime.strptime(item.find('div', class_="date_therm").span.text, "%d.%m.%Y")
        if date >= search_time:
            title_item = item.find_all('p')[0]
            title = title_item.text
            more = f'{site.get("url")[:-12]}{title_item.a["href"]}'
            details = item.find_all('p')[1].text
            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def owen_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news-list'
    items_class_name = 'news-list__item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    news_list = content.find_all("div", class_=items_class_name)

    for item in news_list:
        date = dateparser.parse(item.find("div", class_="news-item-date").text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find("div", class_="news-item__header").text
            more = f'{site.get("url")[:-4]}{item.a["href"][10:]}'
            details = item.find("div", class_="news-item__text").text

            try:
                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers), 'html.parser'
                ).find("div", class_="base-page-text")
                image_url = f'{site.get("url")[:-4]}{more_content.find("img")["src"]}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def bolid_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'cont_inner_right'
    items_class_name = 'news_page'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    news_list = content.find_all("div", class_=items_class_name)

    for item in news_list:
        date = dateparser.parse(item.find("div", class_="news_date").text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            news_text = item.find("div", class_="news_text")
            title = news_text.a["title"]
            details = str(news_text.text).split('\n')[-1].strip()
            more = f'{site.get("url")[:-12]}{news_text.a["href"]}'

            try:
                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers), 'html.parser'
                ).find("div", class_="content_news")
                image_url = f'{site.get("url")[:-12]}{more_content.find("img")["src"]}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def qtech_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "index-news"
    items_class_name = "col-lg-6 col-sm-6"
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    news_list = content.find_all("div", class_=items_class_name)

    for item in news_list:
        date = dateparser.parse(item.find('div', class_="date").text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            more = f'{site.get("url")[:-12]}{item.find("a", "more")["href"]}'

            try:
                image_url = f'{site.get("url")[:-12]}{item.find("img")["src"]}'
            except:
                image_url = None

            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers), 'html.parser'
            ).find("div", class_="news-detail container-content")

            title = more_content.find("h1").text
            details = more_content.find("p").text

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def altonika_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "seminar--list"
    items_class_name = "seminar"
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find("section", class_=content_class_name)
    news_list = content.find_all("article", class_=items_class_name)

    for item in news_list:
        date = dateparser.parse(item.find('time').text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title_item = item.find("h4", class_="seminar__title")
            title = title_item.text
            more = title_item.a["href"]
            details = item.find("div", class_="seminar__paragraph").text

            try:
                image_url = item.find("img", class_="seminar__img")["src"]
            except:
                image_url = None

            if len(image_url) <= 20 or 'pdf' in image_url:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def npf_krug_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "newsWrapper"
    items_class_name = "row news_bl"
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    rows_news_list = content.find_all("div", class_=items_class_name)

    for news_list in rows_news_list:
        for item in news_list.find_all("div", class_="news_section col-md-6"):
            date = dateparser.parse(item.find("div", class_="news_date").text, settings={'TIMEZONE': 'UTC'})
            if date >= search_time:
                title = item.find("div", class_="news_title").text
                details = item.find("div", class_="news_descr").p.text
                image_url = f'{site.get("url")[:-9]}{item.find("div", "news_img").find("img")["data-src"]}'
                more = f'{site.get("url")[:-9]}{item.a["href"]}'

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=more,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))

    return return_news_list


async def mikron_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "row row_flex js-load-more-items"
    items_class_name = "col col_lg_3 col_md_4"
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    news_list = content.find_all("div", class_=items_class_name)

    for item in news_list:
        date = dateparser.parse(item.find("time", class_="b-news-item__date").text, settings={'DATE_ORDER': 'DMY'})
        if date >= search_time:
            title = item.find("p", class_="b-news-item__text").text
            image_url = f'{site.get("url")[:-27]}{item.find("img", "g-hidden")["src"]}'
            more = f'{site.get("url")[:-27]}{item.a["href"]}'
            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers), 'html.parser'
            ).find("div", class_="col col_lg_12").find_all("p")

            try:
                details = more_content[1].text
            except IndexError:
                details = ''

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def macroscop_parser(page_body: str, search_time: datetime,
                           site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "news__list"
    items_class_name = "news__list-item"
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find("ul", class_=content_class_name)
    news_list = content.find_all("li", class_=items_class_name)

    for item in news_list:
        date = dateparser.parse(item.find("div", class_="news__list-item-date caption")
                                .text, settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title_item = item.find("a", class_="news__list-item-title")
            title = title_item.text
            img = item.find("div", "news__list-item-image")["style"].split("\'")[1]
            image_url = f'{site.get("url")[:-7]}{img}'
            more = f'{item.a["href"]}'
            try:
                details = item.find("div", class_="news__list-item-text").p.text
            except:
                details = ''

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def perco_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "tab novosti"
    items_class_name = "news_item"
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    news_list = content.find_all("div", class_=items_class_name)

    for item in news_list:
        date = datetime.strptime(item.find("div", class_="date").text, "%d.%m.%Y")
        if date >= search_time:
            title = item.find("div", class_="name").text.split('\n')[-1]
            image_url = f'{site.get("url")[:-9]}{item.find("img")["src"]}'
            more = f'{site.get("url")[:-9]}{item.a["href"]}'
            details = item.find("div", class_="text").p

            if details is not None:
                details = details.text
            else:
                details = item.find("div", class_="text").text

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def umirs_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    items_class_name = "news-item"
    if items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    news_list = BeautifulSoup(page_body, 'html.parser').find_all("div", class_=items_class_name)

    for item in news_list:
        date = datetime.strptime(item.find("div", class_="news-item-date").text, "%d/%m/%Y")
        if date >= search_time:
            title = item.find("div", class_="news-item-name").a.text
            image_url = f'{site.get("url")[:-6]}{item.find("img")["src"]}'
            more = f'{site.get("url")[:-6]}{item.find("a")["href"]}'
            details = item.find("div", class_="news-item-text").text

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def trevog_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "white_area"
    items_class_name = "news_prewiew"
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    news_list = content.find_all("div", class_=items_class_name)

    for item in news_list:
        date = dateparser.parse(item.find("span", class_="date").text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find("a", class_="title")['title']
            image_url = f'{site.get("url")[:-6]}{item.find("img")["src"]}'
            more = f'{site.get("url")[:-6]}{item.find("a", class_="title")["href"]}'
            details = item.find_all("span")[-1].text

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def tekon_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'table'
    items_class_name = 'news-link'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find('div', id='columns').find(content_class_name)
    headers = content.find_all('p', class_=items_class_name)
    news_body = content.find_all('table')

    if len(headers) != len(news_body):
        raise Exception('Не удалось получить корректные данные от сервера')

    for index in range(len(headers)):
        date = dateparser.parse(headers[index].find("span", class_="news-time").text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = headers[index].find("b").text
            image_url = None
            more = site.get("url")
            details = news_body[index].find_all("td")[-1].text

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def teko_com_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "oformleniecont"
    items_class_name = 'caption col-md-9 col-sm-7'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)
    for item in items:
        date = datetime.strptime(item.find('div').text.strip(), "%d.%m.%Y")
        if date >= search_time:
            title = item.find('h4').a.text
            more = item.find('h4').a['href']
            details = item.p.text

            try:
                more_content = BeautifulSoup(await download(url=more, headers=request_headers), 'html.parser').find(
                    'center')
                image_url = f'{site.get("url")[:-5]}{more_content.find("img")["src"]}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def teko_biz_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "newsList"
    items_class_name = 'publication-block'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)
    for item in items:
        date = datetime.strptime(item.find('p', class_='news-date plain-text').text.strip(), "%d.%m.%Y")
        if date >= search_time:
            title = item.find('h3').text
            more = f'{site.get("url")[:-6]}{item.find("a")["href"]}'

            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers), 'html.parser').find(
                'div', class_='project__content-text news_content_detail')

            try:
                details = ' '.join([p.text.strip() for p in more_content.find_all('p')])
            except:
                details = item.p.text

            try:
                image_url = f'{site.get("url")[:-6]}{more_content.find("img", class_="img-fluid d-block mx-auto")["src"]}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def stels_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "news-list"
    if content_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    items = content.find_all('div')
    for item in items:
        title_item = item.find('h3')
        if title_item is not None:
            title = title_item.text
            more = f'{site.get("url")[:-9]}{title_item.find("a")["href"]}'

            date = datetime.strptime(
                item.find('p', class_='date-time').text.strip().replace('\n', '').replace(' ', '').split('—')[-1],
                "%d.%m.%Y")
            if date >= search_time:
                details = item.find('div', class_='preview-text').text

                try:
                    more_content = BeautifulSoup(await download(url=more, headers=request_headers), 'html.parser') \
                        .find('div', class_='news-detail')
                    image_url = f'{site.get("url")[:-9]}{more_content.find("img")["src"]}'
                except:
                    image_url = None

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=more,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))

    return return_news_list


async def soarco_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "wd-blog-holder blog-pagination-pagination masonry-container wd-spacing-20 row"

    if content_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find("div", class_=content_class_name)
    items = content.find_all('article')
    for item in items:
        more = item.find('div', class_='post-img-wrapp').a['href']

        more_content = BeautifulSoup(await download(url=more, headers=request_headers), 'html.parser') \
            .find('div', class_='article-inner')
        if more_content is None:
            raise Exception('Page parsing failed')
        else:
            day = more_content.find('span', class_='post-date-day').text.strip()
            month = more_content.find('span', class_='post-date-month').text.strip()
            year = datetime.now().year
            date = dateparser.parse(f'{day} {month} {year}', settings={'TIMEZONE': 'UTC'})

            if date >= search_time:
                title = more_content.find('h1', class_='wd-entities-title title post-title').text

                try:
                    details = more_content.find('div', class_='article-body-container').text.strip()
                except:
                    details = None

                try:
                    image_url = more_content.find('figure', class_='entry-thumbnail').find('img')['data-lzl-src']
                except:
                    image_url = None

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=more,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))
    return return_news_list


async def sigur_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news-list-container'
    items_class_name = 'news-list-item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date = datetime.strptime(item.find('div', class_='news-list-item-head__date').text, '%d.%m.%Y')
        if date >= search_time:
            title = item.find('h3', class_='news-list-item__title').text
            more = f'{site.get("url")[:-6]}{item.find("a", class_="news-list-item__link")["href"]}'
            details = item.find('div', class_='news-list-item__content').p.text

            more_content = BeautifulSoup(await download(url=more, headers=request_headers), 'html.parser') \
                .find('div', class_='news-page-image')

            try:
                image_url = f'{site.get("url")[:-6]}{more_content.find("img")["src"]}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def sigma_is_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'bodynews'
    items_class_name = 'bodymainnewsblock'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find('div', id=content_class_name)
    items = content.find_all('div', id=items_class_name)

    for item in items:
        date_text = item.find('span', class_='mainnewsdate').text
        date = datetime.strptime(date_text, '%d.%m.%Y')
        if date >= search_time:
            title = item.a['title']
            more = item.a['href']
            details = item.text.replace(title, '').replace(date_text, '').replace('Подробнее', '')
            if len(details) < 10:
                details = ''

            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def sferasb_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news-sect__content'
    items_class_name = 'news-sect__item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date = datetime.strptime(item.find('div', class_='news-sect__item-time').text, '%d.%m.%Y')
        if date >= search_time:
            title = item.find('div', class_='news-sect__item-title').text
            more = f'{site.get("url")}{item.find("a", class_="def-btn")["href"]}'
            details = item.find('div', class_='news-sect__item-text').text
            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def sensor_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'block-news'
    items_class_name = 'article'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find('div', id=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date = datetime.strptime(item.find('div', class_='article__date').text.strip(), '%d.%m.%Y')
        if date >= search_time:
            title = item.find('div', class_='article__title').a.text
            more = item.find('a')['href']
            details = item.find('div', class_='article__intro').text
            path_image_url: str = item.find("div", class_='article__image has-photo')["style"]
            image_url = f'{site.get("url")[:-5]}' \
                        f'{path_image_url[path_image_url.index("(") + 1: path_image_url.index(")")]}'

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def segnetics_parser(page_body: str, search_time: datetime,
                           site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'main_table'
    items_class_name = 'news_item_date'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find('table', class_=content_class_name)
    date_items = content.find_all('div', class_=items_class_name)
    header_items = content.find_all('div', class_='news_item_header sz6')
    announce_items = content.find_all('div', class_='news_item_announce')

    if len(date_items) != len(header_items) or len(date_items) != len(announce_items):
        raise Exception('Парсеру "segnetics_parser" переданы неккоректные данные')

    for index in range(len(date_items)):
        date = dateparser.parse(date_items[index].text.strip(), settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = header_items[index].text
            more = site.get('url')
            details = ' '.join([p_text.text for p_text in announce_items[index].find_all('p')])

            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def sonarpro_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    items_class_name = 'app__list__news--item'
    if items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    items = BeautifulSoup(page_body, 'html.parser').find_all('div', class_=items_class_name)

    for item in items:
        date = datetime.strptime(item.find('span', class_='date').text, '%d.%m.%Y')
        if date >= search_time:
            title = item.find('h3').text
            more = f'{site.get("url")[:-6]}{item.a["href"]}'
            details = item.find('div', class_='desc-block').p.text
            image_url = f'{site.get("url")[:-6]}{item.find("div", class_="image-block").img["src"]}'

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def rubezh_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'col-lg-4'
    items_class_name = 'col-12 js-show_more--item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    async def get_page_item(url: str):
        download_more = await download(url=more, headers=request_headers)
        more_content = BeautifulSoup(download_more, 'html.parser').find('article', 'page-content')
        return more_content.text + '\n ' + '\n '.join([p.text for p in more_content.find_all('p')])

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find('body')
    items_section_py_4 = content.find('section', class_='py-4').find_all('div', class_=content_class_name)
    items_section_py_6 = content.find('section', class_='py-6').find_all('div', class_=items_class_name)

    for item in items_section_py_4:
        date = datetime.strptime(item.find('div', class_='fs_14 fw-light').text, '%d.%m.%Y')
        if date >= search_time:
            title = item.find('div', class_='list-news__title mt-3').text
            more = f'{site.get("url")[:-12]}{item.a["href"]}'
            image_url = f'{site.get("url")[:-12]}{item.find("img")["src"]}'
            details = await get_page_item(url=more)

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    for item in items_section_py_6:
        date_text: str = item.find('time').text.replace('\t', '').replace('\n', '')
        date = datetime.strptime(date_text, '%d.%m.%Y')
        if date >= search_time:
            title = item.find("a").text
            more = f'{site.get("url")[:-12]}{item.find("a")["href"]}'
            image_url = f'{site.get("url")[:-12]}{item.find("img")["src"]}'
            details = await get_page_item(url=more)

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def rubetek_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news__content news__content_active'
    items_class_name = 'news__item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    list_link = []
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    list_link.append(content.a["href"])

    for a in content.find_all('a', class_=items_class_name):
        list_link.append(a["href"])

    for div in content.find_all('div', class_='news__news-sidebar-text'):
        list_link.append(div.a["href"])

    for link in list_link:
        url = f'{site.get("url")[:-6]}{link}'
        more_page = BeautifulSoup(await download(url=url, headers=request_headers),
                                  'html.parser').find('div', class_='news-internal')

        date = dateparser.parse(more_page.find('div', class_='news-internal__date').text.strip(),
                                settings={'TIMEZONE': 'UTC'})
        if date is not None:
            if date >= search_time:
                title = more_page.find('h1', class_='news-internal__p-title').text
                details = more_page.find('div', class_='news-internal__content').text
                image_url = f'{site.get("url")[:-6]}{more_page.find("img", class_="news-internal__preview-img")["src"]}'

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=url,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))

    return return_news_list


async def rosalinux_parser(page_body: str, search_time: datetime,
                           site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'elementor-widget-container'
    items_class_name = 'premium-blog-post-outer-container'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for link in [item.find('h2', class_='premium-blog-entry-title').a['href'] for item in items]:
        more_page = BeautifulSoup(await download(url=link, headers=request_headers),
                                  'html.parser').find('div', class_='site-content clr')

        date = datetime.strptime(more_page.find('li', class_='meta-date').text.split(':')[1], '%d.%m.%Y')
        if date >= search_time:
            title = more_page.find('h2', class_='single-post-title entry-title').text
            details = more_page.find('div', class_='entry-content clr').text
            # image_url = more_page.find('img', class_='attachment-full size-full wp-post-image')["src"]
            image_url = more_page.find('img', class_='attachment-full')["src"]

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=link,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def ritm_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'work-area-about'
    items_class_name = 'news-list'

    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name).find_all('div',
                                                                                                      class_=items_class_name)

    for div in content:
        link = None
        for a in div.find_all('p'):
            if 'Подробности' in a.text:
                link = a['href']

        downloaded_news_page = await download(url=link, headers=request_headers)
        more_page = BeautifulSoup(downloaded_news_page,
                                  'html.parser').find('div', class_='news-detail')
        date_text = more_page.find('span', class_='news-date-time').text
        date = datetime.strptime(date_text, '%d.%m.%Y')

        if date >= search_time:
            title = div.text[len(date_text) + 1:]
            details = ' '.join([div.text for div in more_page.find_all('div')])

            try:
                if more_page.find("img") is not None:
                    image_url = f'{site.get("url")[:-12]}{more_page.find("img")["src"]}'
                else:
                    image_url = 'https://ritm.ru/bitrix/templates/main/images/slider_0.jpg'

            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=link,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def rgsec_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'site-content pagecont page all_news'
    items_class_name = 'arhive_home_news'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('section', class_=items_class_name)

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'

    async def get_content(items_news) -> list:

        for item in items_news:
            date = dateparser.parse(item.find('div', class_='news_date').span.text.strip(),
                                    settings={'TIMEZONE': 'UTC'})
            if date >= search_time:
                more = item.find("a", class_="box column")["href"]
                if len(urlparse(more).netloc) == 0:
                    more = f'{domain_name}{item.find("a", class_="box column")["href"]}'

                try:
                    try:
                        more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                                     'html.parser').find('div', class_='entry-page-image full_w radius')
                        image_url = more_content.find('img')['src']
                        if len(urlparse(image_url).netloc) == 0:
                            image_url = f'{domain_name}{image_url}'
                    except:
                        image_url = item.find("img")["src"]
                        if len(urlparse(image_url).netloc) == 0:
                            image_url = f'{domain_name}{item.find("img")["src"]}'
                except:
                    image_url = None

                title = item.find('h2').text
                details = item.find('div', class_='news_text drop').text

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=more,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))

        return return_news_list

    return_news_list.extend(await get_content(items))

    return return_news_list


async def red_soft_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    items_class_name = 'blog-post-teaser'
    if items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find_all('div', class_=items_class_name)

    for item in items:
        mass_items = item.find_all('div', class_='row-fluid')
        item_news = mass_items[0]
        item_date = mass_items[1]

        date = dateparser.parse(
            item_date.find(
                'div',
                class_="span12 blog-submitted-teaser text-right text-center-responsive").span["content"].split('T')[0],
            settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title_content = item_news.find('h3', class_='text-center-responsive')
            title = title_content.a.text
            details_items = item_news.find('div', class_='field-item even').find_all('p')
            details = ''
            for p in details_items:
                details = details + p.text + '$new_line$'

            more = title_content.a['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            try:
                try:
                    more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                                 'html.parser').find('ul', class_='slides')
                    image_url = more_content.find('img')['src']
                except:
                    image_url = item_news.find('img')['src']

                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def reallab_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'h1'
    items_class_name = 'mainContent'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    header_news: Tag = BeautifulSoup(page_body, 'html.parser').find(content_class_name)
    table_news = header_news.parent

    p_date = table_news.find_all('p', class_=items_class_name)
    tbody_news = table_news.find_all('tbody')

    for index, item in enumerate(tbody_news):
        date = dateparser.parse(p_date[index].strong.text.strip(), settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            items_news = item.find_all('td')
            img_item = items_news[0]
            news_item = items_news[1]

            title = news_item.find('a', class_='Header2Link').text
            details = news_item.find_all('p')[1].text
            more = news_item.find('a', class_='Header2Link')['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            image_url = img_item.find('img')['src']
            if len(urlparse(image_url).netloc) == 0:
                image_url = f'{domain_name}{image_url}'

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def ramec_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'post post-medium'
    items_class_name = 'post-content'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find_all('article', class_=content_class_name)

    for item in items:
        news_body = item.find('div', class_=items_class_name)
        date = dateparser.parse(news_body.span.text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = news_body.find('h2').a.text
            details = news_body.find('p').text.replace('[...]', '')

            more = news_body.find('h2').a['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}/{more}'

            image_url = item.find('img', class_='img-fluid img-thumbnail rounded-0')['src']
            if len(urlparse(image_url).netloc) == 0:
                image_url = f'{domain_name}{image_url}'

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def prosoftsystems_parser(page_body: str, search_time: datetime,
                                site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'articles'
    items_class_name = 'article'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name).find_all(items_class_name)

    for item in items:
        date = dateparser.parse(item.find('div', class_='date').text.strip(), settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('h2').a.text

            more = item.find('h2').a['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser').find('article', class_='article')

            try:
                try:
                    image_url = more_content.find('img')['src']
                except:
                    image_url = item.find('img')['src']

                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            try:
                details = ''
                for p in more_content.find_all('p'):
                    details = details + p.text + '$new_line$'
            except:
                details = ''

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def prist_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news-list'
    items_class_name = 'desc'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('ul',
                                                         class_=content_class_name).find_all('div',
                                                                                             class_=items_class_name)

    for item in items:
        date = dateparser.parse(item.find('div', class_='date').text.strip(), settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('div', class_='title').a.text

            more = item.find('div', class_='title').a['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}/news/{more}'
            try:
                details = ''
                for p in item.find_all('p'):
                    details = details + p.text + '$new_line$'
            except:
                details = ''

            try:
                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers, timeout=360),
                    'html.parser').find('div', class_='content-side').find('figure').find_all('img')
                image_url = more_content[0]['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def plgn_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'group-content'
    items_class_name = 'row'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('div',
                                                         class_=content_class_name).find_all('div',
                                                                                             class_=items_class_name)

    for item in items:
        date = dateparser.parse(item.find('div', class_='period').span.text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('div', class_='title').a.text
            more = item.find('div', class_='title').a['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'
            try:
                details = ''
                for p in item.find_all('p'):
                    details = details + p.text + '$new_line$'
            except:
                details = ''

            try:
                image_url = item.find('img', class_='img-responsive')['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def parsec_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news common'
    items_class_name = 'article'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find('div', class_='articles-list').find_all('div', class_=items_class_name)

    banner = content.find('div', class_='banner block-radius')
    banner_title = banner.find('h3', 'content__title').a.text
    banner_date = dateparser.parse(banner.find('div', 'content__date').text, settings={'TIMEZONE': 'UTC'})
    banner_details = banner.find('p', 'content__text').text
    banner_tag_a = banner.find('a', 'banner__image js-object-fit')

    banner_img = banner_tag_a.find('img')
    if banner_img is not None:
        banner_img = banner_img['src']

    if len(urlparse(banner_img).netloc) == 0:
        banner_img = f'{domain_name}{banner_img}'

    banner_more = banner_tag_a['href']
    if len(urlparse(banner_more).netloc) == 0:
        banner_more = f'{domain_name}{banner_more}'

    if banner_date >= search_time:
        return_news_list.append(
            ParsedData(site_name=site.get('site_name'),
                       date=banner_date,
                       title=ParserField(is_format=False, text=banner_title),
                       more=banner_more,
                       image_url=banner_img,
                       details=ParserField(is_format=False, text=banner_details)
                       ))

    for item in items:
        date = dateparser.parse(item.find('div', class_='article__date').text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title_data = item.find('h5', class_='article__title')
            title = title_data.text
            more = title_data.parent['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = item.find('p', class_='article__text').text

            try:
                try:
                    more_content = BeautifulSoup(
                        await download(url=more, headers=request_headers, timeout=360),
                        'html.parser').find('div', class_='content').find('div', class_='image')
                    image_url = more_content.find('img')['src']
                except:
                    image_url = item.find('div', class_='article__image').find('img')['src']

                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def osatec_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news-row'
    items_class_name = 'col-xxl-4 col-xl-4 col-md-6 col-sm-6 col-12'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('div',
                                                         class_=content_class_name).find_all('div',
                                                                                             class_=items_class_name)

    for item in items:
        date = dateparser.parse(item.find('p', class_='date').text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('p', class_='caption').text
            more = item.a['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            image_url = item.find('div', class_='image').find('img')['src']
            if len(urlparse(image_url).netloc) == 0:
                image_url = f'{domain_name}{image_url}'

            try:
                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers, timeout=360),
                    'html.parser').find('div', class_='product-description')
                details = ''
                for p in more_content.find_all('p')[1:]:
                    text = p.text.replace('\n', '').strip()
                    if len(text) > 0:
                        details = details + text + '$new_line$'
            except:
                details = ''

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def oni_system_parser(page_body: str, search_time: datetime,
                            site: dict, request_headers: dict) -> List[ParsedData]:
    items_class_name = 'news'
    if items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find_all('div', class_=items_class_name)

    for item in items:
        date = dateparser.parse(item.find('p', class_='date').text.replace(' ', ''), settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('p', class_='title').find('a').text
            details = item.find('p', class_='brief').text
            more = item.find('p', class_='title').find('a')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            try:
                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers, timeout=360),
                    'html.parser').find('div', class_='news-detail')
                image_url = more_content.find('img')['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def octagram_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    items_class_name = 'category-content-container'
    if items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find_all('div', class_=items_class_name)

    for item in items:
        date = dateparser.parse(item.find('div', class_='content-data').find('time').text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('h2', class_='category-content-title').find('a').text
            details = item.find('p').text
            more = item.find('h2', class_='category-content-title').find('a')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            try:
                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers, timeout=360),
                    'html.parser').find('article', class_='content-container')
                image_url = more_content.find('img')['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def astralinux_parser(page_body: str, search_time: datetime,
                            site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news__list row'
    items_class_name = 'news__item--body'
    if items_class_name not in page_body or content_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content_page = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content_page.find_all('div', class_=items_class_name)

    for item in items:
        date = dateparser.parse(item.find('span', class_='briefly briefly--tiny briefly--date').text,
                                settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('a', class_='news__item-title').text
            more = item.find('a', class_='news__item-title')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers, timeout=360),
                'html.parser').find('div', class_='article__content')

            try:
                try:
                    image_url = more_content.find('div', class_='article__preview-item-img--wrap').find('img')['src']
                except:
                    pass
                    # image_url = item.find('div', class_='news-grid-img')['data-load-background']

                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}/{image_url}'
            except:
                image_url = None

            try:
                details = ''
                for p in more_content.find_all('p'):
                    text = p.text.replace('\n', '').strip()
                    if len(text) > 0:
                        details = details + text + '$new_line$'
            except:
                details = ''

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def graviton_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'footer__copyrights'
    items_class_name = 'news-item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').body
    items = content.find_all('div', class_=items_class_name)
    footer_copyrights_date = content.find('div', class_=content_class_name).text.split(' ')[1].split('-')[1]

    for item in items:
        preview_date = item.find('div', class_='preview__date')
        date_text = f'{preview_date.span.text} {preview_date.p.text} {footer_copyrights_date}'
        date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('div', class_='text__title').text
            more = item.find('a', class_='text__more')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers, timeout=360),
                'html.parser').find('div', class_='news-detail__content')

            try:
                image_url = more_content.find('div', class_='news-detail__content--img').find('img')['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            try:
                details = more_content.find('div', class_='news-detail__content--text').text
            except:
                details = ''

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def mcst_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news'
    items_class_name = 'views-row'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('div',
                                                         class_=content_class_name).find_all('div',
                                                                                             class_=items_class_name)

    for item in items:
        date = dateparser.parse(item.find('time').text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('h3').text
            more = item.find('h3').a['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers, timeout=360),
                'html.parser').find('div', class_='content')

            try:
                image_url = more_content.find('img')['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            try:
                details = ''
                for p in more_content.find_all('p'):
                    text = p.text.replace('\n', '').strip()
                    details = details + text + '$new_line$'
            except:
                details = ''

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def eltex_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news_list'
    items_class_name = 'item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('div',
                                                         class_=content_class_name).find_all('div',
                                                                                             class_=items_class_name)

    for item in items:
        date_text = item.find('span', class_='date').text
        date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('a', class_='title').text
            more = item.find('a', class_='title')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = item.find('a', class_='preview_text').text

            try:
                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers, timeout=360),
                    'html.parser').find('div', class_='content_text right_border b-newselement custom-content_text')

                image_url = more_content.find('img')['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def nsgate_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'main'
    items_class_name = 'table'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    items = BeautifulSoup(page_body, 'html.parser').find('table',
                                                         class_=content_class_name).find('p').find_all(items_class_name)

    for index in range(0, len(items) - 1, 2):
        item_header = items[index]
        item_body = items[index + 1]

        header_content = item_header.find_all('td')
        date_text = header_content[1].text

        if date_text == 'Jun - Nov 2021':
            date_text = '7-10-2021'

        date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = header_content[0].text.replace(' \xa0 ', ' ')
            more = site.get('url')

            details = item_body.text
            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def amt_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'content'
    items_class_name = 'article'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name).find_all(items_class_name)

    for item in items:
        date = dateparser.parse(item.find('div', class_='article-date').a.text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('a', class_='article-title').text
            more = item.find('a', class_='article-title')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = item.find('a', class_='article-brief').text
            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def meandr_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'field-item even'
    items_class_name = 'tr'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name).find_all(items_class_name)

    for item in items:
        mass_item = item.find_all('td')
        if len(mass_item) > 1 and 'БЫЛО' not in mass_item[0].text:
            date_item = mass_item[0]
            news_item = mass_item[1]
            date = dateparser.parse(date_item.text, settings={'TIMEZONE': 'UTC'})
            if date >= search_time:
                title = news_item.find('strong')
                if title is not None:
                    title = title.text
                else:
                    title = news_item.find('span')
                    if title is not None:
                        title = title.text
                    else:
                        title = ''

                details = ''
                for div_text in news_item.find_all('div'):
                    text = div_text.text.replace(title, '')
                    details = details + text
                more = site.get('url')

                try:
                    image_url = news_item.find('img')['src']
                    if len(urlparse(image_url).netloc) == 0:
                        image_url = f'{domain_name}{image_url}'
                except:
                    image_url = None

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=more,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))

    return return_news_list


async def aamsystems_parser(page_body: str, search_time: datetime,
                            site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news_table'
    items_class_name = 'tr'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find('table', class_=content_class_name).find_all(items_class_name)

    for item in items:
        mass_item = item.find_all('td')
        if len(mass_item) > 1:
            date_item = mass_item[0]
            news_item = mass_item[1]
            date = dateparser.parse(date_item.find('div', class_='news-date-bold').text, settings={'TIMEZONE': 'UTC'})
            if date >= search_time:
                title = news_item.find('div', class_='news-title').a.text
                more = news_item.find('div', class_='news-title').a['href']
                if len(urlparse(more).netloc) == 0:
                    more = f'{domain_name}{more}'

                details = news_item.find('div', class_='news-detail').text

                try:
                    more_content = BeautifulSoup(
                        await download(url=more, headers=request_headers, timeout=360),
                        'html.parser').find('div', class_='news-detail')
                    image_url = more_content.find('img')['src']

                    if len(urlparse(image_url).netloc) == 0:
                        image_url = f'{domain_name}{image_url}'
                except:
                    image_url = None

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=more,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))

    return return_news_list


async def dssl_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'articles-list lists_block news'
    items_class_name = 'item clearfix item_block'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', items_class_name)

    for item in items:
        date = dateparser.parse(item.find('div', class_='date_small').text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('div', class_='item-title').a.text
            more = item.find('div', class_='item-title').a['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers, timeout=360),
                'html.parser').find('div', class_='news_detail_wrapp big item')

            try:
                # details = more_content.find('div', class_='detail_text').find('p', class_='article-lead').text
                details = ''
                for p in more_content.find_all('p'):
                    details = details + p.text.replace('\n', '').strip() + '$new_line$'
            except:
                details = ''

            try:
                image_url = more_content.find('img')['src']

                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def eltis_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'table'
    items_class_name = 'tr'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body,
                            'html.parser').find('div',
                                                class_='body').find(content_class_name).find(items_class_name)

    items = content.find_all('td')[1].find_all('div')
    for item in items:
        if item.find('h6') is not None:
            date = dateparser.parse(item.find('h6').text, settings={'TIMEZONE': 'UTC'})
            if date >= search_time:
                title = item.find('h5').a.text
                more = item.find('h5').a['href']
                if len(urlparse(more).netloc) == 0:
                    more = f'{domain_name}{more}'

                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers, timeout=360),
                    'html.parser').find('div', class_='news-detail')

                try:
                    details = ''
                    for p in more_content.find_all('p'):
                        details = details + p.text.replace('\n', '').replace('\\xa', '').strip() + '$new_line$'
                except:
                    details = ''

                image_url = None

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=more,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))

    return return_news_list


async def ironlogic_parser(page_body: str, search_time: datetime,
                           site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'index_cat_box news_box'
    items_class_name = 'div'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name).find(items_class_name)
    items = content.find_all(items_class_name)

    for item in items:
        if item.find('span', class_='news_box_t1') is not None:
            date = dateparser.parse(item.find('span', class_='news_box_t1').text, settings={'TIMEZONE': 'UTC'})
        elif item.find('span', class_='news_box_t2') is not None:
            date = dateparser.parse(item.find('span', class_='news_box_t2').text, settings={'TIMEZONE': 'UTC'})
        else:
            date = dateparser.parse(item.find('span', class_='news_box_t3').text, settings={'TIMEZONE': 'UTC'})
        # elif item.find('span', class_='news_box_t2') is not None:
        #     date = dateparser.parse(item.find('span', class_='news_box_t2').text, settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = item.a.text
            more = item.a['href'].replace('..', '')

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}/il_new.nsf{more}'

            if len(item.find_all('span')) > 1:
                details = item.find_all('span')[1].text
            else:
                details = ''

            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def itv_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'ah1 tac tal-md'
    items_class_name = 'li'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('h1', class_=content_class_name).parent.find('ul')
    items = content.find_all(items_class_name)

    for item in items:
        date_text = item.find('p', class_='ah4 tac tal-md').text
        date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('a', class_='link dblock tac tal-md gt-12 mt0-md').text
            more = item.find('a', class_='link dblock tac tal-md gt-12 mt0-md')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers, timeout=360),
                'html.parser').find('div', class_='detail-content')

            try:
                d_content = more_content.text.replace('\r', '').replace('\t', '').replace(title.strip(), '').replace(
                    date_text.strip(), '')
                details = '$new_line$'.join(
                    [' '.join(details_line.strip().split()) for details_line in d_content.split('\n')
                     if len(details_line.strip()) > 0])
            except:
                details = ''

            try:
                image_url = more_content.find('img')['src']
                if '.gif' not in image_url:
                    if len(urlparse(image_url).netloc) == 0:
                        image_url = f'{domain_name}{image_url}'
                else:
                    image_url = None
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def arsenal_sib_parser(page_body: str, search_time: datetime,
                             site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'tab-content'
    items_class_name = 'col-md-1 col-sm-1'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    date_items = content.find_all('div', class_=items_class_name)
    news_items = content.find_all('div', class_='col-md-11 col-sm-11')

    for index in range(len(date_items)):
        date = dateparser.parse(date_items[index].find('span', class_='news_date').text, settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = news_items[index].find('h5').a.text
            more = news_items[index].find('h5').a['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = news_items[index].find('p').text

            try:
                more_content = BeautifulSoup(
                    await download(url=more, headers=request_headers, timeout=360),
                    'html.parser').find('div', class_='page_news')

                image_url = more_content.find('img')['src'].replace('../', '')
                if '.gif' not in image_url:
                    if len(urlparse(image_url).netloc) == 0:
                        image_url = f'{domain_name}{image_url}'
                else:
                    image_url = None
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def elstars_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'text-center'
    items_class_name = 'post-item posts__item row'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('article', class_=items_class_name)

    for item in items:
        date = datetime.strptime(item.find('time', class_='post-item__time').text.strip(), '%d.%m.%Y')
        if date >= search_time:
            title = item.find('header', class_='post-item__header').find('h4').text

            if item.find('header', class_='post-item__header').find('h4').find('a') is not None:
                more = item.find('header', class_='post-item__header').find('h4').find('a')['href']
                if len(urlparse(more).netloc) == 0:
                    more = f'{domain_name}{more}'
            else:
                more = site.get('url')

            details = '$new_line$'.join([p.text.strip() for p in item.find('div').find_all('p')])
            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))
    return return_news_list


async def fastwel_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'mainblock articles items'
    items_class_name = 'article-wide item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date_text = item.find('div', class_='date').text
        date = datetime.strptime(date_text.strip(), '%d.%m.%Y')
        if date >= search_time:
            title = item.find('div', class_='name').find('a').text
            more = item.find('div', class_='name').find('a')['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = item.find('div', class_='text').text.replace(date_text, '').replace(title, '')

            more_content = BeautifulSoup(
                await download(url=more, headers=request_headers, timeout=360),
                'html.parser').find('div', class_='mainblock').find('div', 'image')
            try:
                image_url = more_content.find('img')['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))
    return return_news_list


# async def automiq_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
#     content_class_name = 'listing__list'
#     items_class_name = 'news-card'
#     if content_class_name not in page_body or items_class_name not in page_body:
#         raise Exception(text_exception_class_style)
#
#     return_news_list = []
#
#     domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
#     content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
#     items = content.find_all('div', class_=items_class_name)
#
#     for item in items:
#         date_text = item.find('time', class_='news-card__time').text
#         date = datetime.strptime(date_text.strip(), '%d.%m.%Y')
#         if date >= search_time:
#             title = item.find('h4', class_='news-card__title').text
#             more = item.find('a')['href']
#             if len(urlparse(more).netloc) == 0:
#                 more = f'{domain_name}{more}'
#
#             image_url = item.find('img')['src']
#             if len(urlparse(image_url).netloc) == 0:
#                 image_url = f'{domain_name}{image_url}'
#
#             more_content = BeautifulSoup(
#                 await download(url=more, headers=request_headers, timeout=360),
#                 'html.parser').find('div', class_='page__content content')
#             try:
#                 details = '$new_line$'.join([p.text.strip() for p in more_content.find_all('p')])
#                 if len(details) == 0:
#                     details = more_content.text
#             except:
#                 details = ''
#
#             return_news_list.append(
#                 ParsedData(site_name=site.get('site_name'),
#                            date=date,
#                            title=ParserField(is_format=False, text=title),
#                            more=more,
#                            image_url=image_url,
#                            details=ParserField(is_format=False, text=details)
#                            ))
#     return return_news_list


async def kb_agava_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'col-sm-12'
    items_class_name = 'news_list_wrap'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date_text = item.find('div', class_='news_date').text
        date = datetime.strptime(date_text.strip(), '%d.%m.%Y')
        if date >= search_time:
            title = item.find('div', class_='news_title').a.text
            more = item.find('div', class_='news_title').a['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = '$new_line$'.join(
                [p.text.strip() for p in item.find('div', class_='news_description').find_all('p')])
            image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def keaz_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'article'
    items_class_name = 'info-content__article'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find_all(content_class_name, class_=items_class_name)

    for item in items:
        more = item.find('div', class_='info-content__title info-content__title-link-preview').find('h2').a['href']
        if len(urlparse(more).netloc) == 0:
            more = f'{domain_name}{more}'

        more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360), 'html.parser')
        date_text = more_content.find('head').find('meta')['content'].split(',')[0]
        date = datetime.strptime(date_text.strip(), '%d.%m.%Y')
        if date >= search_time:
            title = more_content.find('h1', class_='title title_h1').text

            article = more_content.find('article', class_='info-content__article')
            details = '$new_line$'.join(
                [p.text.strip() for p in article.find_all('div', class_='info-content__text')[2].find_all('p')]
            )

            try:
                image_url = article.find('img')['src']
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def mzta_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'cck_page_items'
    items_class_name = 'li'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all(items_class_name)

    for item in items:
        news_body = item.find('div', class_='uk-grid').find_all('div', class_='uk-width-1-1')[1]
        date_text = news_body.div.text
        date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = news_body.find('a').text
            details = news_body.text.replace(title, '').replace(date_text, '')
            more = news_body.find('a')['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360), 'html.parser')

            try:
                image_url = more_content.find(
                    'div',
                    class_='uk-card-media-top uk-cover-container').find('a', class_='uk-inline')['href']

                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def nefteavtomatika_parser(page_body: str, search_time: datetime,
                                 site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news__content'
    items_class_name = 'news__content__element'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date_text = item.find('div', class_='news__content__data').text
        date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})
        if date >= search_time:
            title = item.find('a', class_='news__content__text').text
            more = item.find('a', class_='news__content__text')['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360), 'html.parser')
            details = more_content.find('div', class_='page_content__text no_opacity').text

            try:
                image_url = more_content.find(
                    'div',
                    class_='page_content__text no_opacity').find('img')['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def elara_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'newsList'
    items_class_name = 'block'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date_text = item.find('div', class_='date').text
        # date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})
        date = datetime.strptime(date_text.strip(), '%d.%m.%Y')

        if date >= search_time:
            title = item.find('a', class_='title').text
            more = item.find('a', class_='title')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360), 'html.parser')
            news_more_content = more_content.find('div', class_='newsOne').find('div', class_='content')

            details = '$new_line$$new_line$'.join([p.text.replace('\n', '') for p in news_more_content.find_all('p')])

            try:
                image_url = news_more_content.find('img')['src']

                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            except:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def emicon_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'table'
    items_class_name = 'newsdate'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find_all(content_class_name)[0]

    items = content.find_all('p')
    for item in items:
        try:
            next = item['align'] == 'justify'
        except:
            next = False

        if next:
            date_text = item.find('span', class_=items_class_name).text.strip()
            date_mass = date_text.split('.')
            date_value = f'{date_mass[0]}.{date_mass[1]}.20{date_mass[2]}'

            date = datetime.strptime(date_value, '%d.%m.%Y')
            if date >= search_time:
                title = item.find('span', class_='verdana').text
                more = item.find('a', class_='def')['href']
                if len(urlparse(more).netloc) == 0:
                    more = f'{domain_name}{more}'

                more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                             'html.parser')
                details = '$new_line$'.join([p.text for p in more_content.find('p', class_='def').parent.find_all('p')])

                details = details.replace(f'{date_text} - {title}', '')
                details = details.replace(f'{date_value} - {title}', '')

                try:
                    image_url = more_content.find('span', class_='verdana').find('img')['src']
                    if len(urlparse(image_url).netloc) == 0:
                        image_url = f'{domain_name}{image_url}'
                except:
                    image_url = None

                return_news_list.append(
                    ParsedData(site_name=site.get('site_name'),
                               date=date,
                               title=ParserField(is_format=False, text=title),
                               more=more,
                               image_url=image_url,
                               details=ParserField(is_format=False, text=details)
                               ))

    return return_news_list


async def argus_spectr_parser(page_body: str,
                              search_time: datetime,
                              site: dict,
                              request_headers: dict) -> List[ParsedData]:
    content_class_name = 'blog-posts'
    items_class_name = 'ul-blog-post'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find(id=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date_text = item['data-updated']
        date_mass = date_text.split(' ')
        date = dateparser.parse(f'{date_mass[2]}-{date_mass[1]}-{date_mass[3]}', settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = item.find('h3').text
            more = item.find('a', class_='ul-blog-post-title-link')['href']
            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = item.find('div', class_='ul-blog-post-content').h5.text

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser')

            image_content = more_content.find(id='js-blog-post').find('img', class_='img-responsive')
            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def luis_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = "col-lg-9 col-12"
    items_class_name = 'row'

    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('article', class_=items_class_name)

    for item in items:
        date_text = item.find('span', class_='news-list-date').text
        date = datetime.strptime(date_text, '%d.%m.%Y')

        if date >= search_time:
            title = item.find('a', class_='news-list__link').text
            more = item.find('a', class_='news-list__link')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser')
            page_content = more_content.find('div', class_='news-detail__detail-text')

            details = '$new_line$$new_line$'.join(
                [p.text.replace('\n', '').strip() for p in page_content.find_all('p')])

            image_content = page_content.find('img')
            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def insat_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    items_class_name = 'item-news'
    if items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    items = BeautifulSoup(page_body, 'html.parser').find_all('div', class_=items_class_name)

    for item in items:
        date_text = item.find('span', class_='date').text
        date = datetime.strptime(date_text, '%d.%m.%Y')

        if date >= search_time:
            title = item.find('span', class_='name').a.text
            more = item.find('span', class_='name').a['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser')
            page_content = more_content.find('div', class_='block item-content')

            details = '$new_line$$new_line$'.join(
                [p.text.replace('\n', '').strip() for p in page_content.find_all('p')])

            image_content = page_content.find('div', class_='img-product').a
            if image_content is not None:
                # image_url = image_content['src']
                image_url = image_content['href']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def basealt_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'articles'
    items_class_name = 'news_item articletype-0'

    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date_text = item.find('div', class_='date').text
        date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = item.find('a', class_='head').text
            more = item.find('a', class_='head')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = '$new_line$$new_line$'.join(
                [p.text.replace('\n', '').strip() for p in item.find_all('p')])

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser')
            page_content = more_content.find('div', class_='news-text-wrap')
            image_content = page_content.find('img', class_='rte-image')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def teleofis_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'col-xs-8-5 b-events-block'
    items_class_name = 'col-xs-4 b-eb__i'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('article', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date_text = item.find('p', class_='b-eb__i__date').text
        date = dateparser.parse(date_text, settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = item.find('h4', class_='b-eb__i__heading').text
            more = item.find('h4', class_='b-eb__i__heading').a['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = item.find('p', class_='b-eb__i__text').text

            image_content = item.find('img')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def fplus_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'presscenter'
    if content_class_name not in page_body not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('section', class_='presscenter').find('div', class_='row')
    items = list()
    items.append(content.find('div', class_='col-12'))
    items.extend(content.find_all('div', class_='col-6'))
    items.extend(content.find_all('div', class_='col-4 col-md-3'))
    items.extend(content.find_all('div', class_='col-3 col-md-3'))

    for item in items:
        date_text = item.find('span', class_='presscenter-item__date').text
        date = datetime.strptime(date_text, "%d.%m.%Y")

        if date >= search_time:
            title = item.find('span', class_='presscenter-item__name h4_xl').text
            more = item.a['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = '\n'.join([p.text for p in item.find('div', class_='presscenter-item__text').find_all('p')])

            # more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
            #                              'html.parser')
            # page_content = more_content.find('article', class_='article-caption')
            image_content = item.find('img')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}/{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def trei_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'blog'
    items_class_name = 'span12'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:

        date = dateparser.parse(
            item.find('time').text.replace('\n', '').replace('\t', '').split(':')[1][1:],
            settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = item.find('h3').a.text
            more = item.find('p', class_='readmore').a['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            details = item.find('div', class_='item column-1').find('p').text
            image_content = item.find('div', class_='pull-left item-image').find('img')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'

            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def tfortis_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news-list'
    items_class_name = 'news-item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:

        date = dateparser.parse(
            item.find('div', class_='date-subtitle').text, settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = item.find('div', class_='title').text
            more = item.find('a')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser')
            page_content = more_content.find('div', class_='user-content')
            details = page_content.text
            image_content = page_content.find('img')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def automiq_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'listing__list'
    items_class_name = 'news-card'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:

        date = dateparser.parse(
            item.find('time', class_='news-card__time').text, settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = item.find('h4', class_='news-card__title').text
            more = item.find('a', class_='news-card__link')['href']
            image_content = item.find('img', class_='news-card__image')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser')

            page_content = more_content.find('div', class_='page__content content')
            details = page_content.text

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def ridan_parser(page_body: str, search_time: datetime, site: dict, request_headers: dict) -> List[ParsedData]:
    content_class_name = 'block-content__wrapper'
    items_class_name = 'card'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:

        date = dateparser.parse(
            item.find('time', class_='news-info__date').text, settings={'TIMEZONE': 'UTC'})

        if date >= search_time:
            title = item.find('p', class_='card-title').text
            details = item.find('p', class_='card-text').text
            more = item.find('a', class_='card-link')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            image_content = item.find('img')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            print(more)
            print('*' * 100)
            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def elna_severplus_parser(page_body: str,
                                search_time: datetime,
                                site: dict,
                                request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news'
    items_class_name = 'news_item'
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('div', class_=items_class_name)

    for item in items:
        date = datetime.strptime(item.find('span', class_='news_date').text, "%d/%m/%Y")
        if date >= search_time:

            title = item.find('a').text
            more = item.find('a')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser')

            page_content = more_content.find('div', class_='txt')

            details = ' '.join([p.text for p in page_content.find_all('p')])
            image_content = page_content.find('img')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list


async def plazma_t_parser(page_body: str,
                          search_time: datetime,
                          site: dict,
                          request_headers: dict) -> List[ParsedData]:
    content_class_name = 'news-list'
    items_class_name = ('post-11918 post type-post status-publish format-standard has-post-thumbnail hentry '
                        'category-news')
    if content_class_name not in page_body or items_class_name not in page_body:
        raise Exception(text_exception_class_style)

    return_news_list = []

    domain_name = f'{urlparse(site.get("url")).scheme}://{urlparse(site.get("url")).netloc}'
    content = BeautifulSoup(page_body, 'html.parser').find('div', class_=content_class_name)
    items = content.find_all('article', class_=items_class_name)

    for item in items[0: 3]:
        header_news = item.find('h5')
        date_text = f'{header_news.find("span").text}.{datetime.now().strftime("%Y")}'
        date = datetime.strptime(date_text, "%d.%m.%Y")
        if date >= search_time:

            title = header_news.find('a').text
            more = header_news.find('a')['href']

            if len(urlparse(more).netloc) == 0:
                more = f'{domain_name}{more}'

            more_content = BeautifulSoup(await download(url=more, headers=request_headers, timeout=360),
                                         'html.parser')

            page_content = more_content.find('div', class_='entry-content')

            # details = ' '.join([p.text for p in page_content.find_all('p')])
            details = page_content.text
            image_content = page_content.find('img')

            if image_content is not None:
                image_url = image_content['src']
                if len(urlparse(image_url).netloc) == 0:
                    image_url = f'{domain_name}{image_url}'
            else:
                image_url = None

            return_news_list.append(
                ParsedData(site_name=site.get('site_name'),
                           date=date,
                           title=ParserField(is_format=False, text=title),
                           more=more,
                           image_url=image_url,
                           details=ParserField(is_format=False, text=details)
                           ))

    return return_news_list
