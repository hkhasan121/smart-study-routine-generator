from fastapi import APIRouter
from database import get_connection
import random
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

router = APIRouter()

# ======================
# EMAIL CONFIG (CHANGE THIS)
# ======================
SENDER_EMAIL = "hasanmahamud716719@gmail.com"
APP_PASSWORD = "piagkclyijhwyfkk"


def send_otp_email(to_email, otp):
    msg = EmailMessage()
    msg["Subject"] = "Smart Study Routine - OTP Verification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg.set_content(
        f"""
Your OTP for registration is: {otp}

This OTP is valid for 5 minutes.
If you did not request this, please ignore this email.
        """
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)


# ======================
# REGISTER (SEND OTP)
# ======================
@router.post("/register")
def register_user(name: str, email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )
        if cursor.fetchone():
            return {"error": "Email already registered"}

        otp = str(random.randint(100000, 999999))
        expiry = datetime.now() + timedelta(minutes=5)

        cursor.execute(
            """
            INSERT INTO users (name, email, password, is_verified, otp, otp_expiry)
            VALUES (%s, %s, %s, 0, %s, %s)
            """,
            (name, email, password, otp, expiry)
        )
        conn.commit()

        send_otp_email(email, otp)
        return {"message": "OTP sent to your email"}

    finally:
        cursor.close()
        conn.close()

    # 🔐 Generate OTP
    otp = str(random.randint(100000, 999999))
    expiry = datetime.now() + timedelta(minutes=5)

    # 🟡 Insert unverified user
    cursor.execute(
        """
        INSERT INTO users (name, email, password, is_verified, otp, otp_expiry)
        VALUES (%s, %s, %s, 0, %s, %s)
        """,
        (name, email, password, otp, expiry)
    )
    conn.commit()
    conn.close()

    # 📩 Send OTP
    send_otp_email(email, otp)

    return {
        "message": "OTP sent to your email. Please verify to complete registration."
    }


# ======================
# VERIFY OTP
# ======================
@router.post("/verify-otp")
def verify_otp(email: str, otp: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT user_id, otp, otp_expiry
        FROM users
        WHERE email = %s AND is_verified = 0
        """,
        (email,)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return {"error": "Invalid email or already verified"}

    if user["otp"] != otp:
        conn.close()
        return {"error": "Invalid OTP"}

    if datetime.now() > user["otp_expiry"]:
        conn.close()
        return {"error": "OTP expired"}

    # ✅ Verify user
    cursor.execute(
        """
        UPDATE users
        SET is_verified = 1, otp = NULL, otp_expiry = NULL
        WHERE user_id = %s
        """,
        (user["user_id"],)
    )
    conn.commit()
    conn.close()

    return {"message": "Registration successful. You can now login."}


# ======================
# LOGIN (ONLY VERIFIED)
# ======================
@router.post("/login")
def login_user(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT user_id, name, email, is_verified
        FROM users
        WHERE email = %s AND password = %s
        """,
        (email, password)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"error": "Invalid email or password"}

    if user["is_verified"] == 0:
        return {"error": "Please verify OTP before login"}

    return {
        "message": "Login successful",
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"]
    }
