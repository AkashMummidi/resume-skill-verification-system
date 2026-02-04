def extract_certified_skills(cert_text: str, known_skills: set) -> set:
    cert_text = cert_text.lower()
    certified = set()

    for skill in known_skills:
        if skill in cert_text:
            certified.add(skill)

    return certified
