import requests

CF_INFO_URL = "https://codeforces.com/api/user.info"
CF_STATUS_URL = "https://codeforces.com/api/user.status"
CF_RATING_URL = "https://codeforces.com/api/user.rating"


def fetch_cf_data(handle: str):
    """
    Returns:
    {
        rating,
        problems_solved,
        contests
    }
    """

    try:
        # -------------------------
        # 1. Get rating
        # -------------------------
        info_res = requests.get(CF_INFO_URL, params={"handles": handle}, timeout=5).json()

        if info_res["status"] != "OK":
            return {"rating": 0, "problems_solved": 0, "contests": 0}

        user = info_res["result"][0]
        rating = user.get("rating", 0)

        # -------------------------
        # 2. Get submissions → problems solved
        # -------------------------
        status_res = requests.get(CF_STATUS_URL, params={"handle": handle}, timeout=5).json()

        solved_set = set()

        if status_res["status"] == "OK":
            for sub in status_res["result"]:
                if sub.get("verdict") == "OK":
                    problem = sub.get("problem", {})
                    pid = f"{problem.get('contestId')}-{problem.get('index')}"
                    solved_set.add(pid)

        problems_solved = len(solved_set)

        # -------------------------
        # 3. Get contests
        # -------------------------
        rating_res = requests.get(CF_RATING_URL, params={"handle": handle}, timeout=5).json()

        contests = 0
        if rating_res["status"] == "OK":
            contests = len(rating_res["result"])

        return {
            "rating": rating,
            "problems_solved": problems_solved,
            "contests": contests
        }

    except Exception:
        return {"rating": 0, "problems_solved": 0, "contests": 0}