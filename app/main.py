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
    r1, r1o = init._ipdb.is_in_list(ipdb.LOCAL, ip)
    if r1:
        return False, {}
    r2, r2o = init._ipdb.is_in_list(ipdb.BLOCKLIST, ip)
    if r2:
        return True, r2o
    r3, r3o = init._ipdb.is_in_list("ch", ip)
    if not r3:
        return True, r3o
    return False, {}


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
        "type": "ban",
        "value": ""
    }
    e1, e1o = enforce_captcha(ip_str)
    if e1:
        decision["value"] = ip_str
        decision["id"] = e1o["id"]
        return json.dumps([decision,])
    return "null"


if __name__ == '__main__':
    logging.info(f"Starting Garage door notification service")
    app.run(host="0.0.0.0")
