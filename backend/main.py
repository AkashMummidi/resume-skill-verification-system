from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import copy

# --- Utils ---
from utils.pdf_reader import extract_pdf_text_from_bytes
from utils.profile_extractor import extract_profiles
from utils.skill_normalizer import normalize_skills
from utils.resume_skill_extractor import extract_skills_from_resume
from utils.confidence_engine import compute_skill_confidence
from utils.certification_skills_extractor import extract_certified_skills
from utils.project_skills_extractor import extract_project_skills
from utils.github_skills_extractor import extract_github_skills, compute_github_skill_scores
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.suggestion_engine import generate_skill_suggestion
from utils.skill_policy import apply_skill_policy
from utils.cf_analyzer import fetch_cf_data
from utils.cf_confidence_mapping import compute_cf_score
from utils.preparation_planner import generate_preparation_plan
from utils.daily_scheduler import generate_daily_schedule
from utils.reschedule_planner import reschedule_plan

# --- DB ---
from utils.db import users_collection, plans_collection
from utils.auth_utils import hash_password, verify_password


app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELS
# =========================

class User(BaseModel):
    username: str
    password: str


class TaskUpdate(BaseModel):
    username: str
    day: str
    index: int


class RescheduleRequest(BaseModel):
    username: str
    missed_day: int


# =========================
# BASIC ROUTES
# =========================

@app.get("/")
def home():
    return {"status": "Backend running"}


# =========================
# AUTH
# =========================

@app.post("/signup")
def signup(user: User):

    existing = users_collection.find_one({"username": user.username})

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password)
    })

    return {"message": "User registered"}


@app.post("/login")
def login(user: User):

    db_user = users_collection.find_one({"username": user.username})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}


# =========================
# ANALYZE JD (UPDATED)
# =========================

@app.post("/analyze-jd")
async def analyze_jd(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...),
    username: str = Form(...),

    days_until_interview: int = Form(...),
    hours_per_day: int = Form(...),

    # 🔥 NEW
    github_username: str = Form(None),
    github_opt_out: bool = Form(False),

    cf_username: str = Form(None),
    cf_opt_out: bool = Form(False)
):

    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Resume must be PDF")

    if not jd_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="JD must be PDF")

    # -------------------------
    # READ FILES ONCE (CRITICAL FIX)
    # -------------------------
    resume_bytes = await resume_file.read()
    jd_bytes = await jd_file.read()

    # -------------------------
    # Extract text
    # -------------------------
    resume_text = extract_pdf_text_from_bytes(resume_bytes)
    jd_text = extract_pdf_text_from_bytes(jd_bytes)

    # -------------------------
    # Extract profiles (GitHub + CF)
    # -------------------------
    extracted_github, extracted_cf = extract_profiles(resume_bytes, resume_text)

    # 🔥 Fallback logic
    github_username = github_username or extracted_github
    cf_username = cf_username or extracted_cf

    # -------------------------
    # Resume skills
    # -------------------------
    raw_skills = extract_skills_from_resume(resume_text)
    resume_skills = set(normalize_skills(raw_skills))

    project_skills = extract_project_skills(resume_text, resume_skills)
    certified_skills = extract_certified_skills(resume_text, resume_skills)

   # -------------------------
    # GitHub (SMART HANDLING)
    # -------------------------
    if github_opt_out:
        github_username = None
        github_skills = {}

    elif github_username:
        github_data = extract_github_skills(github_username)
        github_skills = compute_github_skill_scores(github_data)

    else:
        github_skills = {}

    # -------------------------
    # Codeforces (SMART HANDLING)
    # -------------------------
    if cf_opt_out:
        cf_username = None
        cf_score = 0

    elif cf_username:
        cf_rating = fetch_cf_data(cf_username)
        cf_score = compute_cf_score(cf_rating)

    else:
        cf_score = 0

    # -------------------------
    # Confidence
    # -------------------------
    raw_confidence_map = {}

    for skill in resume_skills:
        raw_confidence_map[skill] = compute_skill_confidence(
            skill,
            resume_skills,
            project_skills,
            certified_skills,
            github_skills,
            cf_score
        )

    confidence_map = apply_skill_policy(raw_confidence_map)

    # -------------------------
    # JD skills
    # -------------------------
    jd_raw_skills = extract_skills_from_jd(jd_text)
    jd_skills = set(normalize_skills(jd_raw_skills))

    # -------------------------
    # Gap analysis
    # -------------------------
    jd_gap_report = {}

    for jd_skill in jd_skills:
        confidence = confidence_map.get(jd_skill, 0)

        suggestion = generate_skill_suggestion(jd_skill, confidence)

        jd_gap_report[jd_skill] = {
            "confidence": confidence,
            "status": (
                "Missing" if confidence == 0 else
                "Weak Evidence" if confidence < 40 else
                "Moderate Evidence" if confidence < 70 else
                "Strong Evidence"
            ),
            "suggested_action": suggestion
        }

    # -------------------------
    # PLAN GENERATION
    # -------------------------
    plan = generate_preparation_plan(jd_gap_report,days_until_interview,hours_per_day)

    schedule = generate_daily_schedule(
        plan,
        days_until_interview,
        hours_per_day
    )

    schedule = {str(k): v for k, v in schedule.items()}

    # -------------------------
    # SAVE PLAN
    # -------------------------
    plans_collection.insert_one({
        "username": username,
        "jd_skills": list(jd_skills),
        "skill_gap": jd_gap_report,
        "schedule": schedule,
        "days": days_until_interview,
        "hours_per_day": hours_per_day,
        "original_schedule": copy.deepcopy(schedule),  # 🔥 IMPORTANT
        "rescheduled_days": [],
        "github": github_username,
        "codeforces": cf_username,
        "created_at": datetime.utcnow()
    })

    return {
        "daily_tasks": schedule,
        "github": github_username,
        "codeforces": cf_username,
        "jd_gap_report":jd_gap_report,
        "confidence_map":confidence_map
    }


# =========================
# GET PLAN
# =========================

@app.get("/get-plan/{username}")
def get_plan(username: str):

    plan = plans_collection.find_one(
        {"username": username},
        sort=[("created_at", -1)]
    )

    if not plan:
        raise HTTPException(status_code=404, detail="No plan found")

    return {
        "daily_tasks": plan["schedule"],
        "rescheduled_days": plan.get("rescheduled_days", [])
    }




# =========================
# RESCHEDULE
# =========================

@app.post("/reschedule")
def reschedule_api(data: RescheduleRequest):

    import copy

    plan = plans_collection.find_one(
        {"username": data.username},
        sort=[("created_at", -1)]
    )

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    existing_days = plan.get("rescheduled_days", [])

    if data.missed_day in existing_days:
        raise HTTPException(status_code=400, detail="Day already rescheduled")

    # 🔥 ALWAYS start from ORIGINAL schedule
    base_schedule = copy.deepcopy(
        plan.get("original_schedule", plan["schedule"])
    )

    # 🔥 Add new day and sort
    all_rescheduled_days = sorted(existing_days + [data.missed_day])

    new_schedule = base_schedule

    # 🔥 APPLY reschedules one by one (clean replay)
    for day in all_rescheduled_days:
        new_schedule = reschedule_plan(
            schedule=new_schedule,
            skill_gap_report=plan["skill_gap"],
            missed_day=day,
            total_days=len(new_schedule),
            hours_per_day=plan["hours_per_day"]
        )

    plans_collection.update_one(
        {"_id": plan["_id"]},
        {
            "$set": {
                "schedule": new_schedule,
                "rescheduled_days": all_rescheduled_days
            }
        }
    )

    return {"message": "rescheduled"}
    
@app.post("/update-profiles")
async def update_profiles(
    username: str = Form(...),
    github_username: str = Form(None),
    cf_username: str = Form(None)
):

    plan = plans_collection.find_one(
        {"username": username},
        sort=[("created_at", -1)]
    )

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # -------------------------
    # Recompute GitHub
    # -------------------------
    if github_username:
        github_data = extract_github_skills(github_username)
        github_skills = compute_github_skill_scores(github_data)
    else:
        github_skills = {}

    # -------------------------
    # Recompute CF
    # -------------------------
    if cf_username:
        cf_rating = fetch_cf_rating(cf_username)
        cf_score = compute_cf_score(cf_rating)
    else:
        cf_score = 0

    # -------------------------
    # Recompute confidence
    # -------------------------
    resume_skills = set(plan["skill_gap"].keys())

    new_confidence = {}

    for skill in resume_skills:
        new_confidence[skill] = compute_skill_confidence(
            skill,
            resume_skills,
            [],
            [],
            github_skills,
            cf_score
        )

    # -------------------------
    # Regenerate plan
    # -------------------------
    new_plan = generate_preparation_plan(
    plan["skill_gap"],
    plan["days"],
    plan["hours_per_day"]
    )

    new_schedule = generate_daily_schedule(
        new_plan,
        plan["days"],
        plan["hours_per_day"]
    )

    new_schedule = {str(k): v for k, v in new_schedule.items()}

    plans_collection.update_one(
        {"_id": plan["_id"]},
        {
            "$set": {
                "schedule": new_schedule,
                "github": github_username,
                "codeforces": cf_username
            }
        }
    )
    return {"message": "Profiles updated"}

@app.post("/update-task")
def update_task(data: dict):

    username = data.get("username")
    day = str(data.get("day"))
    index = data.get("task_index")
    completed = data.get("completed")

    plan = plans_collection.find_one(
        {"username": username},
        sort=[("created_at", -1)]
    )

    if not plan:
        return {"error": "Plan not found"}

    plan["schedule"][day][index]["completed"] = completed

    plans_collection.update_one(
        {"_id": plan["_id"]},
        {"$set": {"schedule": plan["schedule"]}}
    )

    return {"message": "Task updated"}

@app.post("/delete-resume")
def delete_resume(data: dict):

    username = data.get("username")

    users_collection.update_one(
        {"username": username},
        {"$unset": {"resume_text": ""}}
    )

    return {"message": "Resume deleted"}

@app.delete("/delete-plan/{username}")
def delete_plan(username: str):
    plans_collection.delete_one({"username": username})
    return {"message": "Plan deleted"}