from functools import reduce
from html import unescape
from urllib.parse import unquote

from lxml import etree
from lxml.etree import XPath
from requests import get

from utils import prepare_url
from xml_builder import build_xml

GET_ARTICLE_NAME = XPath("//span[@class='mw-page-title-main']/text()|//h1[@class='page-header__title']/text()")
GET_AUTHOR = XPath("//bdi/text()")
GET_DATE = XPath("//a[contains(@class, 'mw-changeslist-date')]/text()")
GET_CATEGORIES = XPath("//div[@class='page-header__categories']//a[@href]/text()")
# GET_TEXT = XPath("//main//div[@class='quote']/text()|//main//p/text()|//main//h2/text()|//main//h3/text()|//main//a/text()")
# GET_TEXT = XPath("//div[@class='mw-parser-output']/*[./*[not(self::sup)]]/text()")
# GET_TEXT = XPath("//div[@class='mw-parser-output']//p//*[not(self::sup)]/text()|//div[@class='mw-parser-output']//*[not(self::sup)]/a/text()")
# GET_TEXT = XPath("//div[@class='mw-parser-output']/*[not(contains(@id, 'tabs_canon-legend')) and not(name()=aside) and name()=p]/text()|//div[@class='mw-parser-output']/p/*[not(name()=sup)]/text()")
GET_TEXT = XPath(
    "//div[@class='mw-parser-output']/p|//div[@class='mw-parser-output']/h2|//div[@class='mw-parser-output']/h3|//div[@class='mw-parser-output']/h4")


def parse_to_xml(page_url):
    print(f"######### {unquote(page_url)}")
    page = etree.HTML(get(prepare_url(page_url)).content)
    title = GET_ARTICLE_NAME(page)
    if len(title) == 0:
        return None  # Это несуществующая статья

    title = title[0].strip()

    author_page_first = etree.HTML(get(prepare_url(page_url + "?action=history&dir=prev&limit=1")).content)
    author = GET_AUTHOR(author_page_first)[0]
    creation_date = GET_DATE(author_page_first)[0]

    author_page_last = etree.HTML(get(prepare_url(page_url + "?action=history&limit=1")).content)
    last_editor = GET_AUTHOR(author_page_last)[0]
    last_edit_date = GET_DATE(author_page_last)[0]

    category = '/'.join(GET_CATEGORIES(page))

    ch = lambda x: list(map(lambda s: s.replace('\n', ' ').replace('\xa0', ' '), x))
    what1 = list(map(
        lambda p: ch(p.xpath(".//text()")) if not p.tag.startswith('h') else [
            "\n<{}>{}</{}>\n".format(p.tag, ch(p.xpath(".//text()"))[0], p.tag)],
        ps[1:] if len(ps := GET_TEXT(page)) > 1
        else ps
    ))

    text = " ".join(
        filter(
            lambda e: e,
            map(
                lambda line: str(line).strip(),
                reduce(
                    lambda l, r: l + r,
                    what1
                )
            )
        )
    )

    return build_xml(category, author, creation_date, last_editor, last_edit_date, title, text)
