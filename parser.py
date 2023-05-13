from functools import reduce
from urllib.parse import unquote

from lxml import etree
from lxml.etree import XPath
from requests import get

from Article import Article
from utils import prepare_url
from xml_builder import build_xml

GET_ARTICLE_NAME = XPath("//span[@class='mw-page-title-main']/text()|//h1[@class='page-header__title']/text()")
GET_AUTHOR = XPath("//bdi/text()")
GET_DATE = XPath("//a[contains(@class, 'mw-changeslist-date')]/text()")
GET_CATEGORIES = XPath("//div[@class='page-header__categories']//a[@href]/text()")
GET_TEXT = XPath(
    "//div[@class='mw-parser-output']/p"
    "|//div[@class='mw-parser-output']/h2"
    "|//div[@class='mw-parser-output']/h3"
    "|//div[@class='mw-parser-output']/h4"
)


def __clean_text__(text):
    return list(map(lambda string: string.replace('\n', ' ').replace('\xa0', ' '), text))


def __build_header_tag__(element):
    return "\n<{}>{}</{}>\n".format(element.tag, __clean_text__(element.xpath(".//text()"))[0], element.tag)


def __prepared_text__(page):
    split_text = list(
        map(
            lambda element: __clean_text__(element.xpath(".//text()"))
            if not element.tag.startswith('h')
            else [__build_header_tag__(element)],
            all_text[1:]
            if len(all_text := GET_TEXT(page)) > 1
            else all_text
        )
    )

    if len(split_text) == 0:
        return None

    return " ".join(
        filter(
            lambda e: e,
            map(
                lambda line: str(line).strip(),
                reduce(
                    lambda l, r: l + r,
                    split_text
                )
            )
        )
    )


def __get_author_data__(page_url, is_last):
    request = page_url + "?action=history&limit=1"
    if is_last:
        request += "&dir=prev"
    author_page = etree.HTML(get(prepare_url(request)).content)
    author_name = GET_AUTHOR(author_page)[0]
    edit_date = GET_DATE(author_page)[0]
    return author_name, edit_date


def parse_to_xml(page_url):
    try:
        print(f"######### {unquote(page_url)}")
        page = etree.HTML(get(prepare_url(page_url)).content)

        title = GET_ARTICLE_NAME(page)
        if len(title) == 0:
            return None  # Это несуществующая статья
        title = list(filter(lambda t: t.strip(), title))[0]

        author, creation_date = __get_author_data__(page_url, False)

        last_editor, last_edit_date = __get_author_data__(page_url, True)

        category = '/'.join(GET_CATEGORIES(page))

        text = __prepared_text__(page)
        if not text:
            return None

        return build_xml(Article(category, author, creation_date, last_editor, last_edit_date, title, text))
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(e)
        print(f"page_url: {page_url}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return None
