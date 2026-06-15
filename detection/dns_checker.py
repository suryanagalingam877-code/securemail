import dns.resolver

def dns_check(domain):
    try:
        dns.resolver.resolve(domain, "A")
        return True
    except:
        return False