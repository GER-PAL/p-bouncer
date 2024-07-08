import json
import time

from flask import Flask
import app_logger
import logging
from datetime import datetime, timedelta
from threading import Thread
import ipaddress
import schedule

import init
import ipdb
from flask import request
import app_config

request_datetime_list = []
last_update = ""


def remove_old_request_from_list():
    global request_datetime_list
    now = datetime.now()
    threshold = now - timedelta(hours=24)
    request_datetime_list = [dt for dt in request_datetime_list if dt >= threshold]


def enforce_captcha(ip):
    r_is_local, r_local = init._ipdb.is_in_list(ipdb.LOCAL, ip)
    r_is_blocklist, r_blocklist = init._ipdb.is_in_list(ipdb.BLOCKLIST, ip)
    r_is_whitelist, r_whitelist = init._ipdb.is_in_list(ipdb.WHITELIST, ip)
    if r_is_local:
        return False, r_local
    elif r_is_whitelist:
        return False, r_whitelist
    elif r_is_blocklist:
        return True, r_blocklist

    r_country = init._ipdb.search_in_lists(ip)
    if r_country["list"] == app_config.ALLOWED_COUNTRY:
        return False, r_country
    else:
        return True, r_country


app = Flask(__name__)


@app.route("/v1/decisions")
def api_decision():
    global request_datetime_list
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
    request_datetime_list.append(datetime.now())
    if e1:
        decision["value"] = ip_str
        decision["id"] = e1o["id"]
        decision["origin"] = e1o["list"]
        if decision["origin"] == "BLOCK":
            decision["type"] = "ban"
        return json.dumps([decision,])
    return "null"


@app.route("/v1/status")
def api_status():
    global request_datetime_list
    global last_update
    rv = {"ipdb": {}}
    rv["ipdb"]["last_update"] = last_update
    rv["ipdb"]["count"] = init._ipdb.count()
    rv["ipdb"]["count_per_list"] = init._ipdb.count_per_list()
    rv["ipdb"]["request_last_24h"] = len(request_datetime_list)
    return rv


@app.route("/v1/db")
def api_db():
    return init._ipdb.get_db()


def update_lists():
    global last_update
    last_update = str(datetime.now())
    logging.info(f"Rebuilding IPDB")
    init.rebuild()
    logging.info(f"Found {init._ipdb.count()} entries in IPDB")
    remove_old_request_from_list()
    logging.info(f"Found {len(request_datetime_list)} entries in request_last_24h")


schedule.clear()
schedule.every(1).hour.do(update_lists)
#schedule.every(1).minute.do(update_lists)


def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


def startup():
    global last_update
    last_update = str(datetime.now())
    logging.info(f"Building initial IPDB")
    init.rebuild()
    logging.info(f"Found {init._ipdb.count()} entries in IPDB")
    logging.info(f"Starting p-bouncer service")
    thread_schedule = Thread(target=schedule_thread, args=())
    thread_schedule.start()
    return app


if __name__ == '__main__':
    app = startup()
    app.run(host="0.0.0.0")
