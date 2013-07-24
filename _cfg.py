import os

#-- things you have to modify as long as you're on a new comp --#

ANDROID_SDK_PATH_LIS = [
    "/Applications/Android\ Studio.app/sdk/platform-tools",
    "/Applications/Android\ Studio.app/sdk/tools"
]
IOS_PHONEGAP_BIN_PATH = "/Users/nubela/Workspace/phonegap-2.7.0/lib/ios/bin"
ANDROID_PHONEGAP_BIN_PATH = "/Users/nubela/Workspace/phonegap-2.7.0/lib/android/bin"
WATCHER_FILE_PATH = "/Users/nubela/Workspace/transcompiler-watcher/src/watch.py"

#-- some config that i tried to automate, but you can modify as you deem fit --#

CWD = os.getcwd()
DICT_FILE = os.path.join(CWD, "settings.cfg")
METEOR_PORT_RANGE = range(3001, 10000)
WORKSPACE_DIR = os.path.dirname(CWD)
PLOP_PROJECT_PATH = os.path.join(WORKSPACE_DIR, "unifide-plop")
RESOURCES_PATH = os.path.join(CWD, "resources")
WEB_FOLDER_PATH = os.path.join(RESOURCES_PATH, "web")
BITBUCKET_USERNAME = "hello@unifide.sg"
BITBUCKET_PASSWD = "thisisnotsecureatall"

#-- do not fuck below this line unless you know what you are doing --#

REQUIREMENTS = [
    "Flask==0.9",
    "pymongo==2.4.2",
    "flask-login==0.1.3",
    "validate_email==1.1",
    "unidecode==0.04.12",
    "py-lorem==1.2",
    "pil==1.1.7",
]

PROJ_FILES = [
    os.path.join(RESOURCES_PATH, "web.wsgi"),
    os.path.join(RESOURCES_PATH, "run.py"),
    os.path.join(RESOURCES_PATH, "cfg.py"),
    os.path.join(RESOURCES_PATH, "_cfg.py"),
    os.path.join(RESOURCES_PATH, ".gitignore"),
]

BACKEND_CFG = [
    "brand_cfg.py",
    "cfg.py",
]

PLOP_LIBRARIES = [
    "base",
    "campaigns",
    "comments",
    "ecommerce",
    "orders",
    "support",
]