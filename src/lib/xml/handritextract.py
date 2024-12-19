from typing import Iterable, Iterator, Optional, Tuple
from pathlib import Path
from lxml import etree
from lib.manuscripts import CatalogueEntry
from lib.constants import PERSON_DATA_PATH
from lib.people import Person
import lib.utils as utils


log = utils.get_logger(__name__)
nsmap = {None: "http://www.tei-c.org/ns/1.0", 'xml': 'http://www.w3.org/XML/1998/namespace'}


# Region: Persons extracted and delivered

def get_ppl_names() -> list[Person]:
    # This works and gives the correct number of people /SK
    """Delivers the names found in the handrit names authority file.
    Returns list of Person value objects.
    """
    res: list[Person] = []
    tree = etree.parse(PERSON_DATA_PATH, None)
    root = tree.getroot()
    ppl = root.findall(".//person", nsmap)
    for pers in ppl:
        id_ = pers.get('{http://www.w3.org/XML/1998/namespace}id')
        name_tag = pers.find('persName', nsmap)
        all_first_names = name_tag.findall('forename', nsmap)
        all_last_names = name_tag.findall('surname', nsmap)
        first_name_clean = [name.text for name in all_first_names if name.text]
        if first_name_clean:
            first_name = " ".join(first_name_clean)
        else:
            first_name = ""
        last_name = " ".join([name.text for name in all_last_names])
        if not first_name and not last_name and name_tag.text:
            last_name = name_tag.text
        current_pers = Person(id_, first_name, last_name)
        res.append(current_pers)
    return res


# End Region


# Region: Catalog data delivery

def _get_all_data_from_files(files: Iterable[Path]) -> Iterator[CatalogueEntry]:
    for f in files:
        ele = _load_xml_contents(f)
        filename = f.name
        if ele is not None:
            yield _parse_xml_content(ele, filename)


def get_metadata_from_files(files: Iterable[Path]) -> list[CatalogueEntry]:
    data = _get_all_data_from_files(files)
    return list(data)


# End Region
