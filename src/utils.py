resolver = Resolver()
resolver.nameservers = [dns_server]
answers = resolver.query('.', 'NS')
# Not proud of this but it works - we're using a raw DNS query to extract service names
