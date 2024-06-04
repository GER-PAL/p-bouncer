import requests

import app_config as config
import repocollector
import os

import app_config
from ipdb import IpDB
import ipdb

repocollector.create_or_update_repos()

ipv4path = os.path.join(config.WORKDIR_PATH, "country-ip-blocks", "ipv4")

ipv4lists = os.listdir(ipv4path)

_ipdb = IpDB()


def build_geoip(db: IpDB):
    for ipv4list in ipv4lists:
        countryCode = ipv4list.split(".")[0]
        with open(os.path.join(ipv4path, ipv4list), "r") as infile:
            while True:
                line = infile.readline()
                if line == '':
                    break
                oneIpv4 = line.strip()
                db.add(countryCode, oneIpv4)


def build_firehol(db: IpDB):
    for blocklist_url in config.BLOCKLIST_URLS:
        req = requests.get(blocklist_url)
        lines = req.content.decode("utf-8").split("\n")
        for line in lines:
            oneIpv4 = line.strip()
            if oneIpv4 != "" and not oneIpv4.startswith("#"):
                db.add(ipdb.BLOCKLIST, oneIpv4)


build_geoip(_ipdb)
build_firehol(_ipdb)

_ipdb.add(ipdb.LOCAL, "192.168.0.0/16")
_ipdb.add(ipdb.LOCAL, "10.0.0.0/8")
_ipdb.add(ipdb.LOCAL, "172.16.0.0/12")
_ipdb.add(ipdb.LOCAL, "127.0.0.0/24")