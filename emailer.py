#sending an email to the client after booking a Class to their registered Email ID
import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", "no-reply@fitness.local")

def send_email(to_email: str, subject: str, body: str) -> None:
    """
    Send an email via SMTP if configured; otherwise print to console (safe fallback).
    """
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        print("----- [EMAIL-FAKE] -----")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print()
        print(body)
        print("----- [END EMAIL-FAKE] -----")
        return

    msg = EmailMessage()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
        print(f"[EMAIL] Sent to {to_email}")
    except Exception as exc:
        print(f"[EMAIL-ERROR] Could not send email to {to_email}: {exc}")
        print("Email body:\n", body)
