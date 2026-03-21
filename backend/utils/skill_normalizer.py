import re

# 1. Stop words (noise)
STOP_WORDS = {
    "skills", "skill", "education", "project",
    "projects", "computer science", "profile", "computer science","programming",
    "programming languages","web development","web technologies","web app",
    "com","innovative","professional","persist","manage tasks","career development","time management","collaboration",
    "collaborative","teamwork","communication","presentation","problem solve","problem solving","simulations",
    
}

# 2. Alias mapping (normalization)
SKILL_ALIAS_MAP = {
    "js": "javascript",
    "reactjs": "react",
    "nodejs": "node.js",
    "node": "node.js",
    "py": "python",
    "ts": "typescript",
    "golang": "go",
    "postgres": "postgresql",
    "k8s": "kubernetes"
}
VALID_SKILLS = {

    # Programming languages
    "python","java","c","c++","c#","go","rust","kotlin","swift","typescript","javascript","php","ruby","scala","dart","matlab","r","bash","powershell",

    # Backend frameworks
    "django","flask","fastapi","spring","spring boot","express","nestjs","laravel","rails","asp.net","gin","fiber","actix","phoenix",

    # Frontend frameworks
    "react","angular","vue","next.js","nuxt.js","svelte","redux","zustand","tailwind","bootstrap","material ui","chakra ui",

    # Frontend core
    "html","css","sass","less","dom","webpack","vite","babel","eslint","prettier",

    # Databases
    "sql","mysql","postgresql","mongodb","redis","firebase","cassandra","dynamodb","oracle","sqlite","neo4j","elasticsearch",

    # Data engineering
    "hadoop","spark","kafka","airflow","flink","hive","pig","snowflake","databricks",

    # Data science
    "pandas","numpy","scikit-learn","tensorflow","keras","pytorch","matplotlib","seaborn","xgboost","lightgbm",

    # DevOps
    "docker","kubernetes","helm","terraform","ansible","jenkins","github actions","gitlab ci","circleci","travis ci",

    # Cloud platforms
    "aws","azure","google cloud","gcp","lambda","s3","ec2","cloud functions","cloud run",

    # Testing
    "pytest","jest","mocha","chai","selenium","cypress","junit","testng","playwright",

    # Mobile development
    "android","android sdk","kotlin android","swift ios","react native","flutter","xamarin",

    # Networking & security
    "http","https","tcp","udp","tls","oauth","jwt","rest api","graphql","websockets",

    # CS fundamentals
    "data structures","algorithms","operating systems","computer networks","dbms","distributed systems","system design","object oriented programming","design patterns","concurrency",

    # Tools
    "git","github","gitlab","bitbucket","linux","unix","vim","vscode","intellij","postman","jira","notion",

    # Misc
    "microservices","event driven architecture","message queues","rabbitmq","grpc","web scraping","nlp","machine learning","deep learning"
}
def normalize_skills(raw_skills: list):

    normalized = set()

    for skill in raw_skills:

        skill_clean = skill.lower().strip()

        # remove punctuation
        skill_clean = re.sub(r"[^a-z0-9\s]", " ", skill_clean)

        skill_clean = re.sub(r"\s+", " ", skill_clean).strip()

        if skill_clean in STOP_WORDS:
            continue

        # alias normalization
        if skill_clean in SKILL_ALIAS_MAP:
            skill_clean = SKILL_ALIAS_MAP[skill_clean]

        # direct match (multi-word skills)
        if skill_clean in VALID_SKILLS:
            normalized.add(skill_clean)
            continue

        # try detecting multi-word skill phrases
        for valid_skill in VALID_SKILLS:
            if valid_skill in skill_clean:
                normalized.add(valid_skill)

        # fallback: check individual tokens
        tokens = skill_clean.split()

        for token in tokens:

            if token in SKILL_ALIAS_MAP:
                token = SKILL_ALIAS_MAP[token]

            if token in VALID_SKILLS:
                normalized.add(token)

    return sorted(normalized)