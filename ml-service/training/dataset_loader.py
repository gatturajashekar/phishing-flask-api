import pandas as pd


def load_phishtank_dataset():
    """
    Load phishing URLs from PhishTank dataset
    """

    path = "data/raw/verified_online.csv"

    df = pd.read_csv(path)

    urls = df["url"].dropna().tolist()

    return urls


def load_legitimate_dataset():
    """
    Load legitimate domains from Majestic dataset
    """

    path = "data/raw/majestic_million.csv"

    df = pd.read_csv(path)

    # randomly sample domains to avoid dataset bias
    domains = df["Domain"].dropna().sample(5000, random_state=42)

    urls = []

    common_paths = [
        "",
        "/home",
        "/login",
        "/account",
        "/products",
        "/search?q=test",
        "/about",
        "/support",
        "/docs",
        "/blog"
    ]

    for domain in domains:

        for p in common_paths:

            urls.append(f"https://{domain}{p}")
            urls.append(f"https://www.{domain}{p}")

    return urls