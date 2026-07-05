"""
notification.py - Application Notification Service

This file in the Service layer manages triggering alerts and notifications for clients.
Currently:
1. Simulates sending confirmation emails by printing the formatted message to the console.
2. In a production environment, this logic would be integrated with a real SMTP server or external email dispatch services (e.g., SendGrid, Amazon SES).
"""

from datetime import datetime

def send_appointment_email(email_to: str, provider_name: str, start_time: datetime):
    # Simulates sending an email by writing to the console/log.
    # In production, we would use smtplib or a library like fastapi-mail.
    print(f"\n==================================================")
    print(f"📧 SENDING CONFIRMATION EMAIL")
    print(f"To: {email_to}")
    print(f"Subject: Appointment Confirmed!")
    print(f"Message: Hello! Your appointment with {provider_name} "
          f"for {start_time.strftime('%m/%d/%Y at %H:%M')} has been confirmed.")
    print(f"==================================================\n")
