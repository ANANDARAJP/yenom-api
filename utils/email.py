# utils/email.py
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

async def send_email(to_email: str, subject: str, body: str):
    message = MIMEMultipart()
    message["From"] = settings.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Determine TLS settings based on port
    use_tls = settings.SMTP_PORT == 465
    start_tls = not use_tls

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            use_tls=use_tls,
            start_tls=start_tls,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
        )
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

async def send_admin_notification(data):
    subject = "New Contact Form Submission"
    body = f"""
New enquiry received from website.

Name: {data.name}
Email: {data.email}
Phone: {data.phone}
Service: {data.service}

Message:
{data.message}
"""
    await send_email(settings.ADMIN_EMAIL, subject, body)

async def send_auto_reply(data):
    subject = "Thank You for Contacting FT Digital Solutions"
    body = f"""
Hello {data.name},

Thank you for contacting FT Digital Solutions.
We have received your enquiry regarding "{data.service}".
Our team will contact you shortly.

Regards,
FT Digital Solutions
"""
    await send_email(data.email, subject, body)