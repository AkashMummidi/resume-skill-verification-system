def compute_cf_score(
    rating: int
) -> int:
    """
    Compute Codeforces-based evidence score.
    Applies ONLY to CS fundamentals (DSA / Algorithms).
    """

    score = 0

    # ---- Rating-based evidence ----
    if rating >= 1400:
        score += 35
    elif rating >= 1200:
        score += 25
    elif rating >= 1000:
        score += 20
    elif rating >= 700:
        score += 15
    elif rating >= 500:
        score += 10

    # ---- Volume-based evidence (supporting, not dominant) ----
    '''if problems_solved >= 200:
        score += 10
    elif problems_solved >= 100:
        score += 5

    if contests >= 5:
        score += 5'''

    # CF should NEVER overpower other evidence
    return min(score, 40)