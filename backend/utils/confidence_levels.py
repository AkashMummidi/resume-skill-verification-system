def get_confidence_level(score: int) -> str:
    if score == 0:
        return "missing"
    elif score < 40:
        return "low"
    elif score < 70:
        return "medium"
    else:
        return "high"
