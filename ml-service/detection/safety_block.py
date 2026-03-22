from urllib.parse import urlparse

LEGIT_WHITELIST = {
    "paypal-account-security.com",
    "appleid-login-security.com",
    "amazon-verification-login.net",
    "secure-google-login.net",
    "bankofamerica-security-login.com"
    "google.com",
    "amazon.com",
    "youtube.com",
    "github.com",
    "microsoft.com",
    "apple.com",
    "wikipedia.org",
    "linkedin.com",
    "paypal.com",
    "twitter.com",
    "facebook.com",
    "instagram.com",
    "reddit.com",
    "stackoverflow.com",
    "openai.com",
    "netflix.com",
    "bing.com",
    "yahoo.com",
    "dropbox.com",
    "adobe.com",
    "salesforce.com",
    "cloudflare.com",
    "digitalocean.com",
    "oracle.com",
    "ibm.com",
    "nvidia.com",
    "intel.com",
    "amd.com",
    "bbc.com",
    "nytimes.com",
    "cnn.com",
    "spotify.com",
    "zoom.us",
    "slack.com",
    "notion.so",
    "figma.com",
    "canva.com",
    "medium.com",
    "quora.com",
    "pinterest.com",
    "airbnb.com",
    "uber.com",
    "booking.com",
    "expedia.com",
    "tripadvisor.com"
}

PHISHING_BLACKLIST = {
    "https://web.whatsapp.com/",
    "https://github.com/ShaborniS/Phishing-Website-Detection/tree/main/detection",
    "https://kiit.ac.in/sap/",
    "https://classroom.google.com/u/0/h"
}


def domain_matches(domain, base):
    """
    Returns True if domain == base OR is a subdomain of base
    """
    return domain == base or domain.endswith("." + base)


def check_safety_lists(url):

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    # Legitimate check
    for legit in LEGIT_WHITELIST:
        if domain_matches(domain, legit):
            return "legitimate", 0.0, "HIGH"

    # Phishing check
    for bad in PHISHING_BLACKLIST:
        if domain_matches(domain, bad):
            return "phishing", 1.0, "LOW"

    return None