from cfg import TEMPLATE_FOLDER
import os
import jinja2
import unidecode


class MacroStructure:
    FLAT = "flat"
    PORTFOLIO = "portfolio"
    SIMPLE = "simple"
    BIZ_INFO = "biz_info"
    SHOPPING_CART = "shopping_cart"
    TAGGED = "tagged" #TODO


def sluggify(s):
    return unidecode.unidecode(unicode(s)).lower().replace(" ", "_")


def read_template(template_file_name, dic=None):
    if dic is None: dic = {}
    f = open(os.path.join(TEMPLATE_FOLDER, template_file_name), "r")
    template_contents = f.read()
    t = jinja2.Template(template_contents)
    return t.render(**dic)