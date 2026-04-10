def get_confidence_level(score: float) -> str:

    if score < 10:
        return "missing"

    elif score < 30:
        return "low"

    elif score < 60:
        return "medium"

    else:
        return "high"