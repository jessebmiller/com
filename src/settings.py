import os

SITE_ROOT = os.environ.get("SITE_ROOT", os.path.dirname(__file__))
SITE_CONFIG = os.environ.get(
    "SITE_CONFIG",
    "{}/__config__.toml".format(SITE_ROOT),
)
TARGET_ROOT = os.environ.get("TARGET_ROOT", "/out")

