import dns.resolver

FREE_MAIL = ["gmail.com","yahoo.com","outlook.com","hotmail.com"]

def verify_sender(sender, text):

    alerts=[]
    score=0

    if "@" not in sender:
        return 20, ["Invalid sender format"]

    domain = sender.split("@")[1]

    try:
        dns.resolver.resolve(domain,"MX")
    except:
        score+=20
        alerts.append("Sender domain has no mail server")

    brands=["google","paypal","amazon","bank","microsoft"]

    for brand in brands:
        if brand in text.lower() and brand not in domain:
            score+=20
            alerts.append(f"Sender impersonating {brand}")

    if domain in FREE_MAIL:
        score+=5
        alerts.append("Free email provider used")

    return score,alerts