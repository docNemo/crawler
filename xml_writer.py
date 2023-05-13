import os
import uuid

ARTICLES_DIR_PATH = "article"


def write_xml(xml):
    if not os.path.exists(ARTICLES_DIR_PATH):
        os.makedirs(ARTICLES_DIR_PATH)

    xml.write(f"{ARTICLES_DIR_PATH}/{str(uuid.uuid4())}.xml", pretty_print=True, encoding='utf-8')
