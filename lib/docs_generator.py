"""
This library takes in a gen.py config and generates a documentation file
"""
from lib.util import read_template, MacroStructure


def _endpoint_description(endpoint):
    """
    :param endpoint:
    :return description-str:
    """
    dic = {
        "title": endpoint["title"],
        "description": endpoint["description"],
    }
    return read_template("docs/page", dic)


def _part_description(part):
    """
    :param part:
    :return documentation_str:
    """
    if part[1]["structure"] == MacroStructure.FLAT:
        container_dic = {
            "description": part["container"],
            "path_lis": "",
            "container_plural": None,
        }
        container_desc = read_template("docs/flat_part_container", container_dic)
        item_dic = {}

        return "%s\n\n%s" % (container_desc, read_template("docs/flat_part_item", item_dic))
    elif part[1]["structure"] == MacroStructure.PORTFOLIO:
        pass
    elif part[1]["structure"] == MacroStructure.SIMPLE:
        pass
    elif part[1]["structure"] == MacroStructure.TAGGED:
        pass

    return ""


def _gen_docs(endpoint):
    """
    Generates the documentation for this endpoint
    :param endpoint:
    :return doc_str:
    """
    s = "%s\n\n" % (_endpoint_description(endpoint))
    for part in endpoint["parts"]:
        s += "%s\n\n" % (_part_description(part))
    return s


def generate_docs(site):
    s = ""
    for endpoint in site:
        s += _gen_docs(endpoint)
    return s