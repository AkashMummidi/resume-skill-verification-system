import requests

CF_API_URL = "https://codeforces.com/api/user.info"

def fetch_cf_rating(handle: str) -> int:
    """
    Fetch Codeforces rating for a user.
    Returns 0 if user not found or unrated.
    """
    try:
        response = requests.get(CF_API_URL, params={"handles": handle}, timeout=5)
        data = response.json()

        if data["status"] != "OK":
            return 0

        user = data["result"][0]
        user_rating= user.get("rating", 0)
        print(user_rating)
        return user_rating

    except Exception:
        return 0