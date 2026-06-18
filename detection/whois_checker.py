import whois
import datetime
import socket

socket.setdefaulttimeout(10)

def domain_age(domain):
    try:

        data = whois.whois(domain)

        creation = data.creation_date

        if isinstance(creation, list):
            creation = creation[0]

        if not creation:
            return None

        return (
            datetime.datetime.now() - creation
        ).days

    except Exception as e:
        print(f"WHOIS Error: {e}")
        return None