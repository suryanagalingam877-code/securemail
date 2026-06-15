KEYWORDS = [
"verify account",
"urgent action",
"password reset",
"login immediately",
"security alert",
"confirm identity"
]

def keyword_score(text):

    score=0
    hits=[]

    text=text.lower()

    for k in KEYWORDS:
        if k in text:
            score+=5
            hits.append(f"Keyword detected: {k}")

    return score,hits