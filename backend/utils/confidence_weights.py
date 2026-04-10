# =========================
# CONFIDENCE WEIGHTS
# =========================

# Base contributions (fixed signals)
WEIGHTS = {
    "resume": 20,
    "project": 25,
    "certification": 10,
}

# Max cap
MAX_CONFIDENCE = 100

# Scaling factors
GITHUB_MAX_CONTRIBUTION = 25   # GitHub max impact
CF_MAX_CONTRIBUTION = 20       # Codeforces max impact
CF_MAX_RATING = 2000           # normalization cap