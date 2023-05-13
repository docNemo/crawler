from datetime import datetime
from multiprocessing import current_process
from uuid import uuid4

from lxml import etree
from lxml.etree import XPath
from requests import get

from multiprocessor import start_multiprocessing
from parser import parse_to_xml
from properties import START_PAGE, BASE_DOMAIN_FORMAT
from utils import prepare_url
from xml_writer import write_xml

GET_NEXT_NAVIGATION_PAGE_URL = XPath("//div[@class='mw-allpages-nav']/a[starts-with(text(),'Следующая')]/@href")
GET_ARTICLE_URL = XPath("//div[@class='mw-allpages-body']/ul/li[@class='allpagesredirect']/a/@href")


def __get_navigation_page_list__():
    page_url = START_PAGE
    navigation_links = []

    while True:
        navigation_links.append(page_url)
        page_xml = etree.HTML(get(page_url).content)
        next_page_url = GET_NEXT_NAVIGATION_PAGE_URL(page_xml)
        # if len(navigation_links) == 1:
        if len(next_page_url) == 0:
            break
        page_url = BASE_DOMAIN_FORMAT.format(next_page_url[0])

    return navigation_links


def __crawl_pages__(navigation_page_urls, parse, write):
    u = uuid4()
    sum = 0
    print(f"{current_process()} ######### crawl {u} len: {len(navigation_page_urls)}")
    for navigation_page_url in navigation_page_urls:
        navigation_page = etree.HTML(get(prepare_url(navigation_page_url)).content)
        page_urls = GET_ARTICLE_URL(navigation_page)
        print(f"{current_process()} ######### crawl {u} len: {len(page_urls)}")
        sum += len(page_urls)
        # page_urls = ["https://starwars.fandom.com/ru/wiki/Энакин_Скайуокер/Канон"]
        ready_xml_list = filter(lambda el: el, map(parse, page_urls))
        write(list(ready_xml_list))
    print(f"{current_process()} ######### crawl {u} pages: {sum}")


def start():
    start_t = datetime.now()

    navigation_pages = __get_navigation_page_list__()
    print(f"num navigation pages: {len(navigation_pages)}")

    start_multiprocessing(navigation_pages, __crawl_pages__, parse_to_xml, write_xml)

    finish = datetime.now()
    print(f"Total time: {finish - start_t}")
