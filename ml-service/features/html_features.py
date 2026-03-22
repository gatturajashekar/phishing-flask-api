from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_base_domain(domain):
    parts = domain.split(".")
    if len(parts) >= 2:
        return parts[-2] + "." + parts[-1]
    return domain


def extract_html_features(html, base_url):

    features = {}

    # ✅ Handle empty HTML safely
    if html is None:
        features["login_form"] = 0
        features["iframe_count"] = 0
        features["external_link_ratio"] = 0
        features["form_action_external"] = 0
        return features

    soup = BeautifulSoup(html, "html.parser")

    # ==============================
    # 🔹 LOGIN FORM DETECTION
    # ==============================
    password_inputs = soup.find_all("input", {"type": "password"})
    features["login_form"] = 1 if len(password_inputs) > 0 else 0

    # ==============================
    # 🔹 IFRAME DETECTION (FIXED)
    # ==============================
    iframe_count = len(soup.find_all("iframe"))

    # Normalize instead of raw count
    features["iframe_count"] = 1 if iframe_count > 2 else 0

    # ==============================
    # 🔹 EXTERNAL LINK RATIO (FIXED)
    # ==============================
    links = soup.find_all("a", href=True)
    total_links = len(links)

    external_links = 0

    base_domain = urlparse(base_url).netloc
    base_root = get_base_domain(base_domain)

    for link in links:
        href = link["href"]

        # ✅ Ignore relative links
        if not href.startswith("http"):
            continue

        link_domain = urlparse(href).netloc

        if link_domain:
            link_root = get_base_domain(link_domain)

            if link_root != base_root:
                external_links += 1

    if total_links > 0:
        ratio = external_links / total_links

        # smarter scaling
        if ratio > 0.7:
            features["external_link_ratio"] = 1
        elif ratio > 0.3:
            features["external_link_ratio"] = 0.5
        else:
            features["external_link_ratio"] = 0
    else:
        features["external_link_ratio"] = 0

    # ==============================
    # 🔹 FORM ACTION CHECK (FIXED)
    # ==============================
    forms = soup.find_all("form", action=True)

    external_forms = 0

    for form in forms:
        action = form.get("action", "")

        # ignore relative actions
        if not action.startswith("http"):
            continue

        action_domain = urlparse(action).netloc

        if action_domain:
            action_root = get_base_domain(action_domain)

            if action_root != base_root:
                external_forms += 1

    # allow 1 external form (normal), flag only if multiple
    features["form_action_external"] = 1 if external_forms > 1 else 0

    return features