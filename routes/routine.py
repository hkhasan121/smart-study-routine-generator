from fastapi import APIRouter
from database import get_connection
from datetime import date

router = APIRouter()

# ======================
# Weight maps
# ======================
difficulty_map = {
    "easy": 1,
    "medium": 2,
    "hard": 3
}

weakness_map = {
    "low": 1,
    "medium": 2,
    "high": 3
}


# ======================
# Helpers
# ======================
def normalize(value: str, default: str):
    if not value:
        return default
    value = value.strip().lower()
    return value if value else default


def format_time(total_minutes: int):
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours > 0 and minutes > 0:
        return f"{hours} hour {minutes} min"
    elif hours > 0:
        return f"{hours} hour"
    else:
        return f"{minutes} min"


# ======================
# Generate + Save Routine
# ======================
@router.post("/generate-routine")
def generate_routine(user_id: int, total_hours: float):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ Get subjects
    cursor.execute("""
        SELECT subject_id, subject_name, credit, difficulty, weakness
        FROM subjects
        WHERE user_id = %s
    """, (user_id,))
    subjects = cursor.fetchall()

    if not subjects:
        conn.close()
        return {"error": "No subjects found for this user"}

    # 2️⃣ Calculate score
    total_score = 0
    for sub in subjects:
        difficulty = normalize(sub["difficulty"], "medium")
        weakness = normalize(sub["weakness"], "medium")

        score = (
            difficulty_map[difficulty] +
            weakness_map[weakness] +
            sub["credit"]
        )

        sub["score"] = score
        total_score += score

    # 3️⃣ Merge duplicates + calculate minutes
    routine_map = {}

    for sub in subjects:
        minutes = int(round((sub["score"] / total_score) * total_hours * 60))
        subject_key = sub["subject_name"].strip().lower()

        if subject_key in routine_map:
            routine_map[subject_key]["minutes"] += minutes
        else:
            routine_map[subject_key] = {
                "subject_id": sub["subject_id"],
                "subject": sub["subject_name"],
                "minutes": minutes
            }

    # 4️⃣ Save routine
    cursor.execute("""
        INSERT INTO routines (user_id, total_study_time, routine_date)
        VALUES (%s, %s, %s)
    """, (user_id, total_hours, date.today()))
    routine_id = cursor.lastrowid

    # 5️⃣ Save routine details
    for item in routine_map.values():
        cursor.execute("""
            INSERT INTO routine_details (routine_id, subject_id, allocated_time)
            VALUES (%s, %s, %s)
        """, (routine_id, item["subject_id"], item["minutes"]))

    conn.commit()
    conn.close()

    # 6️⃣ Response
    routine_response = []
    for item in routine_map.values():
        routine_response.append({
            "subject": item["subject"],
            "time": format_time(item["minutes"])
        })

    return {
        "message": "Routine generated and saved successfully",
        "routine_id": routine_id,
        "routine": routine_response
    }


# ======================
# Get Routine History
# ======================
@router.get("/routines/{user_id}")
def get_routine_history(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT routine_id, routine_date, total_study_time
        FROM routines
        WHERE user_id = %s
        ORDER BY routine_date DESC
    """, (user_id,))
    routines = cursor.fetchall()

    if not routines:
        conn.close()
        return {"message": "No routines found"}

    history = []

    for r in routines:
        cursor.execute("""
            SELECT s.subject_name, rd.allocated_time
            FROM routine_details rd
            JOIN subjects s ON rd.subject_id = s.subject_id
            WHERE rd.routine_id = %s
        """, (r["routine_id"],))
        details = cursor.fetchall()

        subjects = []
        for d in details:
            subjects.append({
                "subject": d["subject_name"],
                "time": format_time(d["allocated_time"])
            })

        history.append({
            "routine_id": r["routine_id"],
            "date": r["routine_date"],
            "total_hours": r["total_study_time"],
            "subjects": subjects
        })

    conn.close()

    return {
        "user_id": user_id,
        "history": history
    }
@router.delete("/delete-routine/{routine_id}")
def delete_routine(routine_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # delete details first
    cursor.execute(
        "DELETE FROM routine_details WHERE routine_id = %s",
        (routine_id,)
    )

    # delete routine
    cursor.execute(
        "DELETE FROM routines WHERE routine_id = %s",
        (routine_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Routine deleted successfully"}

@router.delete("/delete-all-history/{user_id}")
def delete_all_history(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE rd FROM routine_details rd
        JOIN routines r ON rd.routine_id = r.routine_id
        WHERE r.user_id = %s
    """, (user_id,))

    cursor.execute(
        "DELETE FROM routines WHERE user_id = %s",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "All history deleted"}

