class MacroStructure:
    FLAT = "flat"
    PORTFOLIO = "portfolio"
    SIMPLE = "simple"
    BIZ_INFO = "biz_info"
    SHOPPING_CART = "shopping_cart"
    TAGGED = "tagged" #TODO


SITE = [
    {
        "title": "Index page",
        "description": "Focuses on blablabla..",
        "endpoint": "/",
        "parts": [

            ("Categories", {
                "structure": MacroStructure.FLAT,
                "container": ["Categories"],
                "container_docs": False,
                "container_plural": "Container Holders",
                "item_docs": True,
                "item_description": "Add/Remove/Update a category",
                "mandatory_item_fields": [("name", "Name of the category"),
                                          ("name", "Description of the category")],
                "custom_attr": ("website", "URL of the website"),
                "custom_media": ("brochure", "Brochure for the brand"),
                "paginate": True,
            }),

            ("Mother Categories", {
                "structure": MacroStructure.SIMPLE,
                "container": ["Mother Categories"],
                "description": "Listing of mother categories",
                "mandatory_item_fields": [("name", "Name of the category"),
                                          ("name", "Description of the category")],
                "optional_attr": ("website", "URL of the website"),
                "optional_media": ("brochure", "Brochure for the brand"),
            }),

            ("About EWINS PTE LTD", {
                "structure": MacroStructure.BIZ_INFO,
                "fields": [
                    ("address", "Your address"),
                ],
            }),

        ],
    },

    {
        "title": "Products",
        "description": "mehehehe",
        "endpoint": "/products",
        "parts": [

            ("Products", {
                "structure": MacroStructure.PORTFOLIO,
                "container": ["Products"],
                "description": "Hierachial Listing of products",
                "mandatory_item_fields": [("name", "Name of the category"),
                                          ("name", "Description of the category")],
                "optional_attr": ("website", "URL of the website"),
                "optional_media": ("brochure", "Brochure for the brand"),
                "container_meta": [("name", "Name of the category"),
                                   ("name", "Description of the category")],
                "paginate": True,
            }),

        ],
    },

    {
        "title": "Shopping Cart",
        "description": "mehehehe",
        "endpoint": "/cart",
        "parts": [
            ("Shopping Cart", {
                "structure": MacroStructure.SHOPPING_CART,
            }),
        ],
    },

]


def get_model():
    """
    Encapsulates MODEL and its imports so we don't need to worry about REQUIREMENTS in the plop project
    """
    from base.items.mock import Generate, ItemAttr, ContainerAttr


    MODEL = {
        "Clothings": {
            "containers": Generate.ITEMS_CONTAINERS,
            "items": [
                {
                    "name": "test",
                    "meta": "true",
                    ItemAttr.INSTRUCTIONS: "This is the meta container item."},
                {
                    "custom": Generate.ITEMS_ONLY,
                    "custom_attr": {"brochure_number": range(1, 100)},
                }],
            ContainerAttr.DISCOUNT_PERCENTAGE: "20",
            ContainerAttr.DESCRIPTION: "This container manages your items to sell in your eCommerce store",
        },
    }
    return MODEL


if __name__ == "__main__":
    from base import items
    from base.items.mock import gen_model
    from ecommerce import inventory
    from ecommerce.coupons.mock import gen_container_coupon
    from ecommerce.discounts.mock import gen_discounts


    MODEL = get_model()
    gen_model(MODEL)

    #commerce
    gen_discounts(MODEL)
    gen_container_coupon("asd", 20, items.container_from_path(["Clothings"])._id)
    gen_container_coupon("gdsg", 20, items.container_from_path(["Clothings"])._id)

    #add to inventory
    inventory.add_to_inventory(items.container_from_path(["Clothings"])._id)