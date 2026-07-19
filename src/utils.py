from typing import Optional
from dns.resolver import Resolver

class HealthCheckUtils:
    def __init__(self):
        self.resolver = Resolver()

    def get_nameservers(self):
        self.resolver.nameservers = ['8.8.8.8']  # use a valid DNS server
        return self.resolver

    def query(self, domain: str, record_type: str):
        answers = self.resolver.query(domain, record_type)
        return answers
