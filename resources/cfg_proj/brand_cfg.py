from unifide_backend.action.brand.action import CampaignChannels

BRAND_NAME = "DADA"

CAMPAIGN_CHANNELS = [
    CampaignChannels.FACEBOOK,
    CampaignChannels.TWITTER,
    CampaignChannels.FOURSQUARE,
]

BRAND_MENU = [
    {"order": 0,
     "name": "OVERVIEW",
     "sub-menu":
         [
             {"name": "View All", "link": "/", "order": "0"},
             {"name": "divider", "link": "", "order": "1"},
             {"name": "Facebook", "link": "/facebook/page/activity", "order": "2"},
             {"name": "Twitter", "link": "/twitter/activity", "order": "3"},
             {"name": "Foursquare", "link": "/foursquare/venue/activity", "order": "4"},
             {"name": "Brand Mention", "link": "/brand-mention", "order": "5"},
             {"name": "divider", "link": "", "order": "6"},
             {"name": "Web / Mobile", "link": "/web/campaign/activity", "order": "7"}
         ]},
    {"order": 1,
     "name": "CAMPAIGN",
     "sub-menu":
         [
             {"name": "New Promotion", "link": "/campaign/promo/new", "order": "0"},
             {"name": "New Event", "link": "/campaign/event/new", "order": "1"},
             {"name": "divider", "link": "", "order": "2"},
             {"name": "Manage", "link": "/campaign", "order": "3"}
         ]},
    {"order": 2,
     "name": "MODULES",
     "sub-menu":
         [
             {"name": "Business Info", "link": "/bizinfo", "order": "0"},
             {"name": "Comments", "link": "/comments", "order": "1"},
             {"name": "Orders", "link": "/order", "order": "2"},
             {"name": "divider", "link": "", "order": "3"},
             {"name": "Items", "link": "/items", "order": "4"}
         ]}
]

RESERVED_ITEM_CONTAINERS = {
    "Other Business Info": {
        "description": None,
        "path_lis": ["Other Business Info"],
        "children": {
            "Mobile Maps": {
                "description": "Location Maps for mobile app",
                "path_lis": ["Other Business Info", "Mobile Maps"],
            },

            "Branch Addresses": {
                "description": "For addresses of branches",
                "path_lis": ["Other Business Info", "Branch Addresses"],
            },

            "Opening Hours": {
                "description": "Your Business's Opening Hours",
                "path_lis": ["Other Business Info", "Opening Hours"],
            }
        },
    },

    "Menu": {
        "description": "Manage your menu items here",
        "path_lis": ["Menu"],
    },

    "Specials": {
        "description": "Manage your Specials items here",
        "path_lis": ["Specials"],
    },

    "Pages": {
        "description": "Manage copy for each page",
        "path_lis": ["Pages"],
        "children": {

            "Contact Us": {
                "description": None,
                "path_lis": ["Pages", "Contact Us"],
                "children": {
                    "Emails": {
                        "description": None,
                        "path_lis": ["Pages", "Contact Us", "Emails"],
                    }
                }
            },

            "Specials": {
                "description": None,
                "path_lis": ["Pages", "Specials"],
            },

            "Menu": {
                "description": None,
                "path_lis": ["Pages", "Menu"],
            },

            "Our Story": {
                "description": None,
                "path_lis": ["Pages", "Our Story"],
            },

            "Side Bar": {
                "description": None,
                "path_lis": ["Pages", "Side Bar"],
            },

        },
    }
}