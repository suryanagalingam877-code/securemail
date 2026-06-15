import whois, datetime

def domain_age(domain):
    try:
        w=whois.whois(domain)
        d=w.creation_date
        if isinstance(d,list):
            d=d[0]
        return (datetime.datetime.now()-d).days
    except:
        return None