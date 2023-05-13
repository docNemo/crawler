import logging
from datetime import datetime
from multiprocessing import current_process
from urllib.parse import unquote

from lxml import etree
from lxml.etree import XPath
from requests import get

from multiprocessor import start_multiprocessing
from parser import parse_to_xml
from properties import START_PAGE, BASE_DOMAIN_FORMAT
from xml_writer import write_xml

GET_NEXT_NAVIGATION_PAGE_URL = XPath("//div[@class='mw-allpages-nav']/a[starts-with(text(),'Следующая')]/@href")
GET_ARTICLE_URL = XPath("//div[@class='mw-allpages-body']/ul/li[@class='allpagesredirect']/a/@href")


def __get_page_list__():
    navigation_page_url = START_PAGE
    all_page_urls = []

    while True:
        logging.debug(f"Navigation page: {unquote(navigation_page_url)}")

        navigation_page_xml = etree.HTML(get(navigation_page_url).content)
        all_page_urls += GET_ARTICLE_URL(navigation_page_xml)

        next_navigation_page_url = GET_NEXT_NAVIGATION_PAGE_URL(navigation_page_xml)
        if len(next_navigation_page_url) == 0:
            break

        navigation_page_url = BASE_DOMAIN_FORMAT.format(next_navigation_page_url[0])

    logging.info(f"Number articles: {len(all_page_urls)}")
    return all_page_urls


def __crawl_pages__(page_urls, parse, write):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"{current_process()} ######### len: {len(page_urls)}")
    # page_urls = ["https://starwars.fandom.com/ru/wiki/Энакин_Скайуокер/Канон"]
    # page_urls = ["https://starwars.fandom.com/wiki/Вукипедия:Руководство_для_быстрого_старта"]
    num_articles = 0
    for page_url in page_urls:
        article = parse(page_url)
        if article:
            write(article)
            num_articles += 1

    # ready_xml_list = list(filter(lambda el: el, map(parse, page_urls)))
    # logging.info(f"{current_process()} start write {len(ready_xml_list)} pages")
    # write(ready_xml_list)
    logging.info(f"{current_process()} Finished. Number articles: {num_articles}")


def start():
    logging.basicConfig(level=logging.INFO)

    start_time = datetime.now()
    logging.info(f"Start {start_time}")

    navigation_pages = __get_page_list__()
    logging.debug(f"num navigation pages: {len(navigation_pages)}")
    logging.info(f"Start multiproc: {datetime.now()}")
    start_multiprocessing(navigation_pages, __crawl_pages__, parse_to_xml, write_xml)

    finish_time = datetime.now()
    logging.info(f"Finish {finish_time}")
    logging.info(f"Total time: {finish_time - start_time}")
