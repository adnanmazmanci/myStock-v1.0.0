def tag_headline(text: str) -> str:
    text = text.lower()

    if any(w in text for w in ["fed", "nasdaq", "s&p", "dow", "biden", "yellen", "trump", "us", "america", "republican", "democrat", "white house"]):
        return "US"
    if any(w in text for w in ["ecb", "euro", "germany", "france", "uk", "eu", "europe", "stoxx", "boe", "brexit"]):
        return "Europe"
    if any(w in text for w in ["china", "japan", "asia", "asian", "nikkei", "hang seng", "boj", "korea", "xi", "taiwan"]):
        return "Asia"
    if any(w in text for w in ["oil", "brent", "gold", "commodity", "natural gas", "energy", "copper", "wheat"]):
        return "Commodities"
    if any(w in text for w in ["bitcoin", "crypto", "ethereum", "blockchain", "web3", "altcoin", "defi"]):
        return "Crypto"
    if any(w in text for w in ["türkiye", "tcmb", "lira", "bist", "istanbul", "ankara", "erdoğan", "faiz", "enflasyon"]):
        return "Türkiye"
    
    return "Global"
