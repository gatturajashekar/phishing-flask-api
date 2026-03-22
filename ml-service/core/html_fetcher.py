import requests


def fetch_html(url: str):
    """
    Fetch HTML content from a webpage.
    Returns HTML text or None if failed.
    """
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)

        if response.status_code == 200:
            return response.text

        return None

    except requests.exceptions.RequestException:
        return None