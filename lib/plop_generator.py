"""
This library takes in a gen.py config and generates a plop.py file
"""
import string
from lib.util import sluggify, read_template


class CodeGeneratorBackend:
    """
    Code taken from http://effbot.org/zone/python-code-generator.htm
    """

    def __init__(self):
        self.begin("    ")

    def begin(self, tab="\t"):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return string.join(self.code, "")

    def newline(self):
        self.code.append("\n")

    def write(self, string):
        s = string.split("\n")
        s = filter(lambda x: len(x) > 0, s)
        s = map(lambda x: "%s\n" % (x), s)
        for l in s:
            self.code.append(self.tab * self.level + l)

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError, "internal error in code generator"
        self.level = self.level - 1


def _has_portfolio(endpoint):
    if "parts" in endpoint:
        for p in endpoint["parts"]:
            if p[1]["structure"] == MacroStructure.PORTFOLIO:
                return True
    return False


def _new_fn(c, fn_name, args=None):
    if args is None:
        args = {}

    dic = {"name": fn_name}
    extra_args = []
    for k, v in args.items():
        extra_args += ["%s=%s" % (k, str(v))]
    if len(extra_args) > 0:
        dic["args"] = ", ".join(extra_args)
    c.write(read_template("new_function", dic))
    c.indent()


def _add_flat_data(code_obj, part):
    """
    This function adds code needed to get all the items AND containers from a given container,
    and its child-containers.

    :param code_obj:
    :param part:
    :return:
    """
    ret_var_names = ("%s_all_items", "%s_all_containers")
    id = sluggify(part[0])
    container_path_lis = str(part[1]["container"])
    vars = {"container_path_lis": container_path_lis,
            "dic_name": "dic",
            "id": id}
    code_obj.write(read_template("flat", vars))
    code_obj.newline()
    ret_var_names = map(lambda x: x % (id), ret_var_names)
    return ret_var_names


def _add_simple_data(code_obj, part):
    ret_var_names = ("%s_all_items", "%s_container_obj")
    id = sluggify(part[0])
    container_path_lis = str(part[1]["container"])
    vars = {"container_path_lis": container_path_lis,
            "id": id, }
    code_obj.write(read_template("simple", vars))
    code_obj.newline()
    ret_var_names = map(lambda x: x % (id), ret_var_names)
    return ret_var_names


def _add_portfolio_data(code_obj, part):
    ret_var_names = ("%s_container_of_choice", "%s_all_items")
    id = sluggify(part[0])
    container_path_lis = str(part[1]["container"])
    vars = {"container_path_lis": container_path_lis,
            "id": id, }
    code_obj.write(read_template("portfolio", vars))
    code_obj.newline()
    ret_var_names = map(lambda x: x % (id), ret_var_names)
    return ret_var_names


def _add_shopping_cart_data(code_obj, part):
    ret_var_names = (
        "discount_amount",
        "coupon_amount",
        "shopping_cart_items",
        "order",
        "cashback_rule",
        "cashback_amt",
        "shipping_items",
    )
    code_obj.write(read_template("shopping_cart"))
    code_obj.newline()
    return ret_var_names


def _add_tagged_data(code_obj, part):
    #todo
    pass


def _gen_endpoint_part(code_obj, part):
    if part[1]["structure"] == MacroStructure.FLAT:
        return _add_flat_data(code_obj, part)
    elif part[1]["structure"] == MacroStructure.PORTFOLIO:
        return _add_portfolio_data(code_obj, part)
    elif part[1]["structure"] == MacroStructure.SIMPLE:
        return _add_simple_data(code_obj, part)
    elif part[1]["structure"] == MacroStructure.TAGGED:
        return _add_tagged_data(code_obj, part)
    elif part[1]["structure"] == MacroStructure.SHOPPING_CART:
        return _add_shopping_cart_data(code_obj, part)


def _gen_endpoint(code_obj, endpoint):
    """
    Generates a plop endpoint

    :param code_obj:
    :param endpoint:
    :return:
    """
    #begin function
    fn_name = endpoint["title"].lower().replace(" ", "_")
    code_obj.write(read_template("route", {"endpoint": endpoint["endpoint"], "methods": "'GET'"}))

    if _has_portfolio(endpoint):
        arrity_endpoint = "%s/<path:path>" % (endpoint["endpoint"])
        code_obj.write(read_template("route", {"endpoint": arrity_endpoint, "methods": "'GET'"}))
        _new_fn(code_obj, fn_name, {"path": None})
    else:
        _new_fn(code_obj, fn_name)

    #data parts
    vars = []
    if "parts" in endpoint:
        for part in endpoint["parts"]:
            possible_vars = _gen_endpoint_part(code_obj, part)
            if possible_vars is not None:
                vars += list(possible_vars)

    #return a render_template
    code_obj.write(read_template("dic", {"vars": vars}))
    code_obj.write(read_template("render_template", {"template_name": fn_name, "dic_name": "dic"}))
    code_obj.dedent()
    code_obj.newline()
    code_obj.newline()


def generate_plop(site):
    """
    Returns the string of the python code (minus the imports)
    :param site:
    :return:
    """
    c = CodeGeneratorBackend()
    for endpoint in site:
        _gen_endpoint(c, endpoint)
    return c.end()
