import logging
from multiprocessing import current_process
from re import sub
from urllib.parse import unquote

from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import XPath
from requests import get

import properties
from Article import Article
from utils import prepare_url
from xml_builder import build_xml

GET_TITLE = XPath("//span[@class='mw-page-title-main']/text()|//h1[@class='page-header__title']/text()")
GET_AUTHOR = XPath("//bdi/text()")
GET_DATE = XPath("//a[contains(@class, 'mw-changeslist-date')]/text()")
GET_CATEGORIES = XPath("//div[@class='page-header__categories']//a[@href]/text()")
GET_TEXT = XPath("//div[@class='mw-parser-output']")
IGNORE_CATEGORIES = [
    "",
    "Заготовки о персоналиях из реального мира",
    "Шаблоны юзербоксов",
    "Веб-сайты",
    "Мультимедийные проекты",
    "Заготовки об источниках информации",
    "Заготовки о языках",
    "Заготовки"
]


def __clean_text(text):
    return list(map(lambda string: string.replace('\n', ' ').replace('\xa0', ' '), text))


def clean_str(string):
    return sub(r"(\s)+", r"\g<1>", string.strip())


def __prepared_text(page):
    raw_text = GET_TEXT(page)
    if len(raw_text) == 0:
        return None

    content = etree.tostring(raw_text[0])
    content_soup = BeautifulSoup(content, 'lxml')

    text_without_tags = content_soup.get_text()
    return clean_str(text_without_tags)


def __get_creator_data(page_url):
    request = page_url + properties.CREATOR_REQUEST_PARAM
    creator_page = etree.HTML(get(prepare_url(request)).content)
    creator_name = GET_AUTHOR(creator_page)[0]
    creation_date = GET_DATE(creator_page)[0]
    return creator_name, creation_date


def parse_to_xml(page_meta):
    page_url, primary_title = page_meta
    logging.info(f"{current_process()} ######### {unquote(page_url)}")
    page = etree.HTML(get(prepare_url(page_url)).content)

    title = list(filter(lambda t: t.strip(), GET_TITLE(page)))
    if len(title) == 0:
        return None  # Это несуществующая статья

    text = __prepared_text(page)
    if not text:
        return None  # Это несуществующая статья

    creator, creation_date = __get_creator_data(page_url)

    raw_categories = GET_CATEGORIES(page)
    if len(raw_categories) == 0:
        return None

    for cat in raw_categories:
        if cat.strip() in IGNORE_CATEGORIES:
            return None

    categories = '/'.join(raw_categories)

    return build_xml(Article(categories, creator, creation_date, primary_title, text))
