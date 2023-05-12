import uuid


def write_xml(xmls):
    for file in xmls:
        file.write(f"article/{str(uuid.uuid4())}.xml", pretty_print=True, encoding='utf-8')
