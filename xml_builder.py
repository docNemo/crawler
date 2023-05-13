from lxml import etree
from lxml.etree import ElementTree

from Article import Article

CDATA_FORMAT = "<![CDATA[{}]]>"


def __add_auto_attrib__(elem):
    elem.set("auto", "true")
    elem.set("type", "str")
    elem.set("verify", "true")


def build_xml(article: Article):
    category_el = etree.Element("category")
    category_el.text = article.get_category()
    __add_auto_attrib__(category_el)

    author_el = etree.Element("author")
    author_el.text = article.get_author()
    __add_auto_attrib__(author_el)

    creation_date_el = etree.Element("creation_date")
    creation_date_el.text = article.get_creation_date()
    __add_auto_attrib__(creation_date_el)

    last_editor_el = etree.Element("last_editor")
    last_editor_el.text = article.get_last_editor()
    __add_auto_attrib__(last_editor_el)

    last_edit_date_el = etree.Element("last_edit_date")
    last_edit_date_el.text = article.get_last_edit_date()
    __add_auto_attrib__(last_edit_date_el)

    title_el = etree.Element("title")
    title_el.text = article.get_title()
    __add_auto_attrib__(title_el)

    text_el = etree.Element("text")
    text_el.text = CDATA_FORMAT.format(article.get_text())
    __add_auto_attrib__(text_el)

    outer_xml = etree.Element("doc")
    outer_xml.append(title_el)
    outer_xml.append(category_el)
    outer_xml.append(author_el)
    outer_xml.append(creation_date_el)
    outer_xml.append(last_editor_el)
    outer_xml.append(last_edit_date_el)
    outer_xml.append(text_el)

    return ElementTree(outer_xml)
