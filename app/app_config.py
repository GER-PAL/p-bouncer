import os


def get_environ_variable_or_exit(name):
    if name not in os.environ:
        raise Exception(f"Missing {name} in ENVIRONMENT variables")
    return os.environ[name]

BLOCKLIST_NAME = "BLOCK"

REPOS = [
    {"url": "https://github.com/herrbischoff/country-ip-blocks"}
]

BLOCKLIST_URL = "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"

WORKDIR_PATH = "workdir"

PUBLIC_PATH = "public"
