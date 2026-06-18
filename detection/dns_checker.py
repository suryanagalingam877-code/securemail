import dns.resolver

def dns_check(domain):
    try:
        dns.resolver.resolve(domain, "A")
        return True

    except dns.resolver.NXDOMAIN:
        return False

    except dns.resolver.NoAnswer:
        return False

    except dns.resolver.Timeout:
        return False

    except Exception:
        return False