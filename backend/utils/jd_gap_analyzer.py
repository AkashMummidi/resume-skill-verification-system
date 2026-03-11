def analyze_jd_skill_gap(
    jd_skills: set[str],
    resume_skills: set[str],
    confidence_map: dict[str, int]
) -> dict:
    report = {}

    for skill in jd_skills:
        if skill not in resume_skills:
            report[skill] = {
                "status": "Missing",
                "confidence": 0,
            }
        else:
            confidence = confidence_map.get(skill, 0)

            if confidence < 30:
                report[skill] = {
                    "status": "Weak Evidence",
                    "confidence": confidence,
                }
            elif confidence < 70:
                report[skill] = {
                    "status": "Moderate Evidence",
                    "confidence": confidence,
                }
            else:
                report[skill] = {
                    "status": "Strong Evidence",
                    "confidence": confidence,
                }

    return report
