def rule_based_detection(features, url):

    score = 0

    suspicious_keywords = [
        "login",
        "verify",
        "account",
        "secure",
        "update",
        "signin",
        "bank",
        "paypal"
    ]

    url_lower = url.lower()

    # IP address in URL
    if features["has_ip"]:
        score += 4

    # @ symbol
    if features["has_at_symbol"]:
        score += 3

    # hyphen in domain
    if features["hyphen_in_domain"]:
        score += 2

    # too many subdomains
    if features["subdomain_count"] >= 3:
        score += 2

    # missing HTTPS
    if features["https"] == 0:
        score += 2

    # suspicious words
    for word in suspicious_keywords:
        if word in url_lower:
            score += 2
            break

    # login form detected
    if features["login_form"]:
        score += 2

    # external links
    if features["external_link_ratio"] > 0.5:
        score += 2

    # external form action
    if features["form_action_external"]:
        score += 3

    if score >= 4:
        return "phishing", score

    return "legitimate", score
def apply_rules(url, html, features=None):
    if features is None:
        return 0

    label, score = rule_based_detection(features, url)
    return score