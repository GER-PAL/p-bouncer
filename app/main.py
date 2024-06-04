import json

from flask import Flask
import app_logger
import logging
from datetime import datetime, timedelta
from threading import Thread
import ipaddress

import init
import ipdb
from flask import request


def enforce_captcha(ip):
    r_is_local, r_local = init._ipdb.is_in_list(ipdb.LOCAL, ip)
    r_is_blocklist, r_blocklist = init._ipdb.is_in_list(ipdb.BLOCKLIST, ip)
    if r_is_local:
        return False, r_local
    elif r_is_blocklist:
        return True, r_blocklist

    r_country = init._ipdb.search_in_lists(ip)
    if r_country["list"] == "ch":
        return False, r_country
    else:
        return True, r_country


app = Flask(__name__)


@app.route("/v1/decisions")
def api_decision():
    ip_str = request.args.get('ip')
    decision = {
        "duration": "23h0m0.0s",
        "id": "1",
        "origin": "na",
        "scenario": "na",
        "scope": "Ip",
        "type": "captcha",
        "value": ""
    }
    e1, e1o = enforce_captcha(ip_str)
    if e1:
        decision["value"] = ip_str
        decision["id"] = e1o["id"]
        decision["origin"] = e1o["list"]
        return json.dumps([decision,])
    return "null"


if __name__ == '__main__':
    logging.info(f"Starting Garage door notification service")
    app.run(host="0.0.0.0")
