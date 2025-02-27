import os
from dotenv import load_dotenv

load_dotenv()


def get_environ_variable_or_exit(name):
    if name not in os.environ:
        raise Exception(f"Missing {name} in ENVIRONMENT variables")
    return os.environ[name]


BLOCKLIST_NAME = "BLOCK"

REPOS = [
    {"url": "https://github.com/herrbischoff/country-ip-blocks"}
]

BLOCKLIST_URLS = ["https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"
                  ,"https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level2.netset"]

WORKDIR_PATH = "workdir"

PUBLIC_PATH = "public"

IP_WHITELIST = get_environ_variable_or_exit("WHITELIST")

IP_WHITELIST2_URL = get_environ_variable_or_exit("WHITELIST2_URL")

ALLOWED_COUNTRY = get_environ_variable_or_exit("ALLOWED_COUNTRY")

