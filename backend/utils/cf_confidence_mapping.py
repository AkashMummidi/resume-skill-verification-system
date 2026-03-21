def compute_cf_score(cf_data):

    rating = cf_data["rating"]
    solved = cf_data["problems_solved"]
    contests = cf_data["contests"]

    # -------------------------
    # Normalize each factor
    # -------------------------

    rating_score = min(rating / 2000, 1) * 50     # max 50
    solved_score = min(solved / 300, 1) * 30      # max 30
    contest_score = min(contests / 50, 1) * 20    # max 20

    total_score = rating_score + solved_score + contest_score

    return round(total_score)