import ipaddress

BLOCKLIST = "BLOCK"
LOCAL = "LOCAL"


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

    def is_in_list(self, list_name: str, ip_str: str):
        ip = ipaddress.ip_address(ip_str)
        if ip in self.cache:
            return self.cache[ip]["match"], self.cache[ip]
        for subnet in self._db[list_name]:
            if ip in ipaddress.ip_network(subnet):
                if ip not in self.cache:
                    self.cache[ip] = {"id": self.next_id(), "list": list_name, "match": True}
                return True, self.cache[ip]
        if ip not in self.cache:
            self.cache[ip] = {"id": self.next_id(), "list": list_name, "match": False}
        return False, self.cache[ip]
