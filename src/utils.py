resolver = Resolver()
resolver.nameservers = ['8.8.8.8']  # use a valid DNS server
answers = resolver.query('.', 'NS')