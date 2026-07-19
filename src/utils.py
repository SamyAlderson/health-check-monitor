import dns.resolver

class Resolver:
    def __init__(self):
        self.nameservers = []

    def query(self, name, record_type):
        try:
            return dns.resolver.resolve(name, record_type)
        except dns.resolver.NoAnswer:
            return []

# Not proud of this but it works - we're using a raw DNS query to extract service names
resolver = Resolver()
resolver.nameservers = [dns_server]
answers = resolver.query('.', 'NS')