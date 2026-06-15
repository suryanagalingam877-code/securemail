BRANDS = ["google","paypal","amazon","bank","microsoft"]

def brand_mismatch(text, domains):

    alerts=[]
    text=text.lower()

    for brand in BRANDS:
        if brand in text:
            for d in domains:
                if brand not in d:
                    alerts.append(f"Brand mismatch: {brand}")

    return alerts