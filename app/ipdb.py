import datetime
import ipaddress

BLOCKLIST = "BLOCK"
LOCAL = "LOCAL"
WHITELIST = "ALLOW"


class IpDB:

    def __init__(self):
        self._db = {}
        self.cache = {}
        self._id_counter = 100

    def add(self, section: str, ip: str):
        if section not in self._db:
            self._db[section] = []
        self._db[section].append(ip)

    def next_id(self):
        icc = self._id_counter
        self._id_counter += 1
        return icc

    def clear(self):
        self._db = {}

    def count(self):
        c = 0
        for k,v in self._db.items():
            c += len(v)
        return c

    def count_per_list(self):
        c_per = {}
        for k, v in self._db.items():
            c_per[k] = len(v)
        return c_per

    def is_in_list(self, list_name: str, ip_str: str):
        ip = ipaddress.ip_address(ip_str)
        if ip in self.cache and self.cache[ip]["list"] == list_name:
            return True, self.cache[ip]
        for subnet in self._db[list_name]:
            if ip in ipaddress.ip_network(subnet):
                if ip not in self.cache:
                    self.cache[ip] = {"id": self.next_id(), "list": list_name, "match": True, "created": datetime.datetime.now()}
                return True, self.cache[ip]
        return False, {}

    def get_db(self):
        return self._db

    def truncate_cache(self):
        if len(self.cache) < 10000:
            return
        older_then = datetime.datetime.now() - datetime.timedelta(days=1)
        old_entries = [x for x in self.cache.keys() if self.cache[x]["created"] < older_then]
        print(f"Deleting {len(old_entries)}")
        for oe in old_entries:
            self.cache.pop(oe, None)

    def search_in_lists(self, ip_str: str):
        self.truncate_cache()
        ip = ipaddress.ip_address(ip_str)
        if ip in self.cache:
            return self.cache[ip]
        for list_key in [x for x in self._db.keys() if x != LOCAL and x != BLOCKLIST]:
            for subnet in self._db[list_key]:
                if ip in ipaddress.ip_network(subnet):
                    if ip not in self.cache:
                        self.cache[ip] = {"id": self.next_id(), "list": list_key, "match": True, "created": datetime.datetime.now()}
                    return self.cache[ip]
        if ip not in self.cache:
            self.cache[ip] = {"id": self.next_id(), "list": "N/A", "match": False, "created": datetime.datetime.now()}
        return self.cache[ip]
