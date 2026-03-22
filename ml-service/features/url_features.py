import re
from urllib.parse import urlparse


def extract_url_features(url: str) -> dict:

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    path = parsed.path

    if path == "/":
        path = ""

    features = {}

    features["url_length"] = len(url)

    # ✅ strict IP detection
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    features["has_ip"] = 1 if re.match(ip_pattern, domain) else 0

    features["has_at_symbol"] = 1 if "@" in url else 0

    features["hyphen_in_domain"] = 1 if "-" in domain else 0

    parts = domain.split(".")
    features["subdomain_count"] = max(len(parts) - 2, 0)

    features["https"] = 1 if parsed.scheme == "https" else 0

    features["path_length"] = len(path)

    # safe digit ratio
    digit_count = sum(c.isdigit() for c in url)
    features["digit_ratio"] = digit_count / len(url) if len(url) > 0 else 0

    # ✅ better special char detection
    special_chars = re.findall(r"[@%&$!#]", url)
    features["special_char_ratio"] = len(special_chars) / len(url) if len(url) > 0 else 0

    features["high_digit_ratio"] = 1 if features["digit_ratio"] > 0.15 else 0

    features["long_url"] = 1 if len(url) > 75 else 0

    features["hostname_length"] = len(domain)

    # ✅ normalized token count
    tokens = re.split(r"[.-]", domain)
    token_count = len(tokens)
    features["domain_token_count"] = 1 if token_count > 3 else 0

    # 🔥 optional strong features
    features["contains_login"] = 1 if "login" in url.lower() else 0
    features["contains_verify"] = 1 if "verify" in url.lower() else 0

    trusted_domains = [
    "google.com",
    "youtube.com",
    "amazon.com",
    "facebook.com",
    "instagram.com",
    "whatsapp.com",
    "microsoft.com",
    "microsoftonline.com",
    "github.com",
    "linkedin.com",
    "twitter.com",
    "x.com",
    "apple.com",
    "icloud.com",
    "netflix.com",
    "stackoverflow.com",
    "reddit.com",
    "quora.com",
    "yahoo.com",
    "bing.com",
    "openai.com",
    "chat.openai.com",
    "aws.amazon.com",
    "azure.microsoft.com",
    "cloud.google.com",
    "mongodb.com",
    "paypal.com",
    "stripe.com",
    "flipkart.com",
    "snapdeal.com",
    "zomato.com",
    "swiggy.com",
    "ola.com",
    "uber.com",
    "zoom.us",
    "skype.com",
    "dropbox.com",
    "drive.google.com",
    "docs.google.com",
    "gmail.com",
    "outlook.com",
    "protonmail.com",
    "canva.com",
    "figma.com",
    "notion.so",
    "medium.com",
    "wordpress.com",
    "wikipedia.org",
    "bbc.com",
    "cnn.com"
]

    features["is_trusted_domain"] = 1 if any(domain.endswith(d) for d in trusted_domains) else 0

    return features