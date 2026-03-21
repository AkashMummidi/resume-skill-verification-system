import copy

def reschedule_plan(
    schedule,
    skill_gap_report,
    missed_day,
    total_days,
    hours_per_day
):

    # Convert keys → int
    original = {int(k): v for k, v in schedule.items()}

    # 🔥 Deep copy to avoid mutation bugs
    original = copy.deepcopy(original)

    new_schedule = {}

    # -------------------------
    # Copy before missed day
    # -------------------------
    for day in range(1, missed_day):
        new_schedule[day] = original.get(day, [])

    # -------------------------
    # Mark skipped day
    # -------------------------
    new_schedule[missed_day] = [
        {
            "task": "Day Skipped",
            "skill": "",
            "time": "",
            "completed": False,
            "skipped": True
        }
    ]

    # -------------------------
    # SHIFT forward
    # -------------------------
    for day in range(missed_day + 1, total_days + 1):
        new_schedule[day] = original.get(day - 1, [])

    # Convert back to string keys
    return {str(k): v for k, v in new_schedule.items()}