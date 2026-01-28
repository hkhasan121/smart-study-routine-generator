from fastapi import APIRouter
from database import get_connection

router = APIRouter()

# =============================
# ADD SUBJECT (duplicate protected)
# =============================
@router.post("/add-subject")
def add_subject(
    user_id: int,
    subject_name: str,
    credit: int,
    difficulty: str,
    weakness: str
):
    conn = get_connection()
    cursor = conn.cursor()

    # Check duplicate subject per user
    cursor.execute(
        "SELECT COUNT(*) FROM subjects WHERE user_id=%s AND LOWER(subject_name)=%s",
        (user_id, subject_name.lower())
    )
    if cursor.fetchone()[0] > 0:
        conn.close()
        return {"error": "Subject already added"}

    cursor.execute(
        """
        INSERT INTO subjects (user_id, subject_name, credit, difficulty, weakness)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, subject_name.lower(), credit, difficulty.lower(), weakness.lower())
    )
    conn.commit()
    conn.close()

    return {"message": "Subject added successfully"}


# =============================
# GET ALL SUBJECTS (for list)
# =============================
@router.get("/subjects/{user_id}")
def get_subjects(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT subject_id, subject_name, credit, difficulty, weakness FROM subjects WHERE user_id=%s",
        (user_id,)
    )
    subjects = cursor.fetchall()
    conn.close()

    return subjects


# =============================
# UPDATE SUBJECT
# =============================
@router.put("/update-subject/{subject_id}")
def update_subject(
    subject_id: int,
    subject_name: str,
    credit: int,
    difficulty: str,
    weakness: str
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE subjects
        SET subject_name=%s, credit=%s, difficulty=%s, weakness=%s
        WHERE subject_id=%s
        """,
        (subject_name.lower(), credit, difficulty.lower(), weakness.lower(), subject_id)
    )
    conn.commit()
    conn.close()

    return {"message": "Subject updated successfully"}


# =============================
# DELETE SUBJECT
# =============================
@router.delete("/delete-subject/{subject_id}")
def delete_subject(subject_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM subjects WHERE subject_id=%s",
        (subject_id,)
    )
    conn.commit()
    conn.close()

    return {"message": "Subject deleted successfully"}
