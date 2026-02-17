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
                "reason": "Required by JD but not present in resume",
                "suggested_action": f"Learn {skill} fundamentals and syntax"
            }
        else:
            confidence = confidence_map.get(skill, 0)

            if confidence < 30:
                report[skill] = {
                    "status": "Weak Evidence",
                    "confidence": confidence,
                    "reason": "Mentioned but lacks supporting evidence",
                    "suggested_action": f"Build a project demonstrating {skill}"
                }
            elif confidence < 70:
                report[skill] = {
                    "status": "Moderate Evidence",
                    "confidence": confidence,
                    "reason": "Some evidence found, depth unclear",
                    "suggested_action": f"Improve depth and real-world usage of {skill}"
                }
            else:
                report[skill] = {
                    "status": "Strong Evidence",
                    "confidence": confidence,
                    "reason": "Skill well supported by evidence",
                    "suggested_action": f"Explore advanced use-cases of {skill}"
                }

    return report
