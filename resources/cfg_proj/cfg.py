import os
from base import S3

#-- UPDATE THIS SECTION --#

DOMAIN = "http://localhost:5000"

#-- things below should not be touched unless you know what you are doing (sane defaults) --#

CWD = os.path.dirname(os.path.realpath(__file__))
DEBUG = True
ASSETS_FOLDER = os.path.join(CWD, "base", "assets")
MOCK_MODE = False
LOG_FILE = os.path.join(CWD, "log.txt")
INSTALLED_PACKAGES = [
    "articles",
    "campaigns",
    "ecommerce",
    "orders",
    "items",
]

#mongodb
# MONGO_URI = 'mongodb://localhost/unifide'         #auto generated below
MONGO_HOST = "localhost"
MONGO_PORT = 27017
# MONGO_DB = "dada"                                 #auto generated below
if MOCK_MODE:
    MONGO_DB = "mock"

#mock stuff
MOCK_DATE_RANGE_DAYS = 100

#facebook app info
FB_APP_ID = "336489173138188"
FB_APP_SECRET = "b259ee37fdb0acb61feb1b1af0fdab57"
FB_REDIRECT_URI = "http://127.0.0.1:3000/"
FB_PERMS = ["manage_pages", "publish_stream"]
FB_REALTIME_TOKEN = "thisisnotsecureatall1987"

#twitter app info
TW_CONSUMER_KEY = "dB4v3wKk52LIRz6SRSZTJQ"
TW_CONSUMER_SECRET = "IkfpGDZteinlSBY3iNKwrtuEarB6sZA8U6rbZXJ7h4U"
TW_REDIRECT_URI = "http://127.0.0.1:3000/"
ADD_USER_MAX_TWEET = 800

#foursquare app info
FSQ_CLIENT_ID = "DMJY0SMIR5050PMBOL2JKLQWO2R4NCMILNSHMM5VBDJH2AQH"
FSQ_CLIENT_SECRET = "0EYFVQNM2KTF4V11BS2PZKOPWV2DOBUG1GUHV3D5HOH0SPQO"
FSQ_REDIRECT_URI = "http://127.0.0.1:3000/"

# API Packages to be enabled
API_TO_REGISTER = (
    "social_connect",
    "account",
    "campaign",
    "brand_mention",
    "items",
    "business",
    "order",
)

#facebook app info
FB_APP_ID = "336489173138188"
FB_APP_SECRET = "b259ee37fdb0acb61feb1b1af0fdab57"
FB_REDIRECT_URI = "http://localhost:3000/account/auth/facebook/"
FB_PERMS = ["manage_pages", "publish_stream", "create_event"]
FB_REALTIME_TOKEN = "thisisnotsecureatall1987"

#twitter app info
TW_CONSUMER_KEY = "dB4v3wKk52LIRz6SRSZTJQ"
TW_CONSUMER_SECRET = "IkfpGDZteinlSBY3iNKwrtuEarB6sZA8U6rbZXJ7h4U"
TW_REDIRECT_URI = "http://127.0.0.1:3000/account/auth/twitter/"
TW_INDIVIDUAL_STREAM = True
ADD_USER_MAX_TWEET = 50

#foursquare app info
FSQ_CLIENT_ID = "DMJY0SMIR5050PMBOL2JKLQWO2R4NCMILNSHMM5VBDJH2AQH"
FSQ_CLIENT_SECRET = "0EYFVQNM2KTF4V11BS2PZKOPWV2DOBUG1GUHV3D5HOH0SPQO"
FSQ_REDIRECT_URI = "http://127.0.0.1:3000/account/auth/foursquare/"

#brand_mention alerts info
GOOGLE_USERNAME = 'unifidetest@gmail.com'
GOOGLE_PASSWD_ENCODED = 'BZh91AY&SYE\xf2\x04j\x00\x00\x08\x81\x80*e\x9e\x00 \x001\x03@\xd0"`\xd4\xcc\x86[L\x88\xbc\x8d@\xb0\tp\xbb\x92)\xc2\x84\x82/\x90#P'

#amazon s3
AWS_ACCESS_KEY_ID = 'AKIAIYOWWMY2JWOT7YAA'
AWS_SECRET_ACCESS_KEY = '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'
S3_BUCKET_NAME = "ctrleff"
S3_BUCKET_CHECK = False
S3_KEY_NAME = "ctrleff"
S3_LOCATION = S3.Location.SG
CLOUDFRONT_URL = "http://d1boersyg287yp.cloudfront.net/"

#local uploads
UPLOAD_FOLDER = os.path.join(CWD, "resources")
UPLOAD_METHOD = "local" #or s3
UPLOAD_RELATIVE_ENDPOINT = "resources"

#campaigns
DOMAIN_PATH = "http://www.unifide.sg/"
URL_IGNORE_KEYWORD = [
    "and",
    "a",
    "an",
    "the",
    "on"
]
CAMPAIGN_TYPE = [
    "facebook",
    "twitter",
    "foursquare",
    "web",
    "blog"
]

#-- configuration below are generated automatically by script --#