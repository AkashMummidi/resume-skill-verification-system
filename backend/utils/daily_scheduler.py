from datetime import datetime, timedelta

BLOCK_SIZE = 60


def generate_time_slots(start_hour, blocks_per_day):
    slots = []
    current = datetime(2024, 1, 1, start_hour, 0)

    for _ in range(blocks_per_day):
        end = current + timedelta(minutes=BLOCK_SIZE)

        slots.append({
            "start": current.strftime("%H:%M"),
            "end": end.strftime("%H:%M")
        })

        current = end

    return slots


def generate_daily_schedule(tasks, days, hours_per_day, start_hour=9):

    blocks_per_day = hours_per_day

    schedule = {}

    task_index = 0

    for day in range(1, days + 1):

        slots = generate_time_slots(start_hour, blocks_per_day)
        schedule[day] = []

        for slot in slots:

            # no more tasks
            if task_index >= len(tasks):
                break

            task = tasks[task_index]

            schedule[day].append({
                "task": task["task"],
                "skill": task["skill"],
                "time": f"{slot['start']} - {slot['end']}",
                "completed": False
            })

            #  handle multi-block tasks
            task["blocks"] -= 1

            if task["blocks"] == 0:
                task_index += 1

    return schedule