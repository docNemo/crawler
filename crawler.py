from lxml import etree
from requests import get

import parser
import properties
from lxml.etree import XPath

from utils import prepare_url
from xml_writer import write_xml

GET_NEXT_NAVIGATION_PAGE_URL = XPath("//div[@class='mw-allpages-nav']/a[starts-with(text(),'Следующая')]/@href")
GET_ARTICLE_URL = XPath("//div[@class='mw-allpages-body']/ul/li[@class='allpagesredirect']/a/@href")


def get_navigation_page_list():
    page_url = properties.START_PAGE
    navigation_links = []

    while True:
        navigation_links.append(page_url)
        page_xml = etree.HTML(get(page_url).content)
        next_page_url = GET_NEXT_NAVIGATION_PAGE_URL(page_xml)
        # if len(next_page_url) == 0:
        if len(navigation_links) == 1:
            break
        page_url = properties.BASE_DOMAIN_FORMAT.format(next_page_url[0])

    return navigation_links


def crawl_pages(navigation_page_urls, parse, write_xml):
    for navigation_page_url in navigation_page_urls:
        navigation_page = etree.HTML(get(prepare_url(navigation_page_url)).content)
        # page_urls = GET_ARTICLE_URL(navigation_page)
        page_urls = ["https://starwars.fandom.com/ru/wiki/Энакин_Скайуокер/Канон"]
        ready_xml_list = filter(lambda el: el, map(parse, page_urls))
        write_xml(list(ready_xml_list))


def start():
    navigation_pages = get_navigation_page_list()
    crawl_pages(navigation_pages, parser.parse_to_xml, write_xml)
