import logging
from datetime import datetime
from multiprocessing import current_process
from urllib.parse import unquote

from lxml import etree
from lxml.etree import XPath
from requests import get

import properties
from multiprocessor import start_multiprocessing
from parser import parse_to_xml
from properties import START_PAGE, BASE_DOMAIN_FORMAT
from xml_writer import write_xml

GET_NEXT_NAVIGATION_PAGE_URL = XPath("//div[@class='mw-allpages-nav']/a[starts-with(text(),'Следующая')]/@href")
GET_ARTICLE_URL = XPath("//div[@class='mw-allpages-body']//a[not(contains(@class,'mw-redirect'))]")


def __get_page_list__():
    navigation_page_url = START_PAGE
    all_page_urls = []

    while True:
        logging.debug(f"Navigation page: {unquote(navigation_page_url)}")

        navigation_page_xml = etree.HTML(get(navigation_page_url).content)
        all_page_urls += list(
            map(
                lambda el: (el.attrib["href"], el.text),
                GET_ARTICLE_URL(navigation_page_xml)
            )
        )

        next_navigation_page_url = GET_NEXT_NAVIGATION_PAGE_URL(navigation_page_xml)
        if len(next_navigation_page_url) == 0:
            break

        navigation_page_url = BASE_DOMAIN_FORMAT.format(next_navigation_page_url[0])

    logging.info(f"Number articles: {len(all_page_urls)}")
    return all_page_urls


def __crawl_pages__(page_urls, parse, write):
    logging.basicConfig(level=properties.LOG_LEVEL)
    logging.info(f"{current_process()} ######### len: {len(page_urls)}")
    num_articles = 0
    for page_url in page_urls:
        article = parse(page_url)
        if article:
            write(article)
            num_articles += 1
            logging.info(f"{current_process()} - {round(num_articles / len(page_urls) * 100, 3)}%")

    logging.info(f"{current_process()} Finished. Number articles: {num_articles}")


def start():
    logging.basicConfig(level=properties.LOG_LEVEL)

    start_time = datetime.now()
    logging.info(f"Start {start_time}")

    pages = __get_page_list__()
    logging.info(f"Num pages: {len(pages)}")
    logging.info(f"Start multiproc: {datetime.now()}")
    start_multiprocessing(pages, __crawl_pages__, parse_to_xml, write_xml)

    finish_time = datetime.now()
    logging.info(f"Finish {finish_time}")
    logging.info(f"Total time: {finish_time - start_time}")
