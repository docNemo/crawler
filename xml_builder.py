from lxml import etree
from lxml.etree import ElementTree


def build_xml(
        category,
        author,
        creation_date,
        last_editor,
        last_edit_date,
        title,
        text
):
    category_el = etree.Element("category")
    category_el.text = category

    author_el = etree.Element("author")
    author_el.text = author

    creation_date_el = etree.Element("creation_date")
    creation_date_el.text = creation_date

    last_editor_el = etree.Element("last_editor")
    last_editor_el.text = last_editor

    last_edit_date_el = etree.Element("last_edit_date")
    last_edit_date_el.text = last_edit_date

    title_el = etree.Element("title")
    title_el.text = title

    text_el = etree.Element("text")
    text_el.text = text  # todo CDATA

    outer_xml = etree.Element("doc")
    outer_xml.append(title_el)
    outer_xml.append(category_el)
    outer_xml.append(author_el)
    outer_xml.append(creation_date_el)
    outer_xml.append(last_editor_el)
    outer_xml.append(last_edit_date_el)
    outer_xml.append(text_el)

    return ElementTree(outer_xml)
