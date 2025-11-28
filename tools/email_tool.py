def send_email_notification(user_email: str, subject: str, body: str) -> str:
    """
    Mocks sending an email via Twilio/SendGrid.
    """
    # Hackathon Mock: Just print it or return success
    print(f"--- MOCK EMAIL SENT ---")
    print(f"To: {user_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print(f"-----------------------")
    return "Email sent successfully."