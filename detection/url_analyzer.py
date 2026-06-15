import re
import tldextract

def extract_domains(text):

    urls = re.findall(r'https?://\S+', text)
    domains = []

    for url in urls:
        ext = tldextract.extract(url)
        domains.append(ext.domain + "." + ext.suffix)

    return domains