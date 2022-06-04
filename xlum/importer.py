import os
from lxml import etree
import logging

from data.classes import XlumMeta

def from_xlum(file_path:os.PathLike) -> XlumMeta:
    """import data from an *.xlum file

    Args:
        file_path (os.PathLike): path to the file

    Returns:
        XlumMeta: structured data, see: xlum.data.classes for a description of the dataclasses
    """    
    assert os.path.exists(file_path), f"{file_path=} not found"
    assert file_path.split(".")[-1].lower() == "xlum", f"{file_path.split('.')[-1]} invalid, expected '.xlum'"
    
    with open("assets/xlum_schema.xsd") as f:
        xsd =f.read()

    xsd_source = etree.XML(
        xsd
    )
    schema = etree.XMLSchema(xsd_source)
    parser = etree.XMLParser(schema = schema)


    # Import XML-like data
    try:
        tree:etree.ElementTree = etree.parse(file_path, parser)
    except etree.XMLSyntaxError as ex:
        logging.warning(type(ex), ex)
        tree = etree.parse(file_path)
    logging.debug(f"{tree}\nfrom: {file_path=}")



    return _extract_xlum(tree)

def _extract_xlum(tree:etree.ElementTree) -> XlumMeta:
    """extract XLum meta data from an importet element tree

    Args:
        tree (etree.ElementTree): xlum file as element tree

    Returns:
        XlumMeta: parsed data
    """
    root:etree.Element = tree.getroot()
    assert root.tag.lower() == 'xlum', f"{root.tag=}, expected 'xlum'"

    for k in root.attrib:
        print(k, root.attrib[k])
    return XlumMeta.from_element_tree(tree)