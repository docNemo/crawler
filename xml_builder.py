from lxml import etree
from lxml.etree import ElementTree

from Article import Article


def __add_auto_attrib(elem):
    elem.set("auto", "true")
    elem.set("type", "str")
    elem.set("verify", "true")


def __append(parent, name, value):
    element = etree.Element(name)
    element.text = etree.CDATA(value)
    __add_auto_attrib(element)
    parent.append(element)


def build_xml(article: Article):
    article_xml = etree.Element("doc")
    __append(article_xml, "categories", article.get_categories())
    __append(article_xml, "creator", article.get_creator())
    __append(article_xml, "creation_date", article.get_creation_date())
    __append(article_xml, "title", article.get_title())
    __append(article_xml, "text", article.get_text())

    return ElementTree(article_xml)
