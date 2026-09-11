import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import EMAIL_HOST, EMAIL_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD


async def send_welcome_email(email: str, name: str):

    subject = "Welcome to Employee Management System"

    body = f"""
    
    Hi {name},
    
    your Employee account has been Created
    
    Regards
    Employee Management Syatem Team """

    await send_email(email, subject, body)


async def send_otp_email(email: str, otp: str):

    subject = "Your Login OTP For Employee Management System"

    body = f"""
    
    Hello,
    
    your OTP is : {otp} valid for 1 Minute
    
    Regards
    Employee Management Syatem Team """

    await send_email(email, subject, body)


async def send_email(email: str, subject: str, body: str):

    message = MIMEMultipart()

    message["From"] = EMAIL_ADDRESS
    message["To"] = email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:

            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, message.as_string())
            print(f"{subject} email has been sent TO : {email} !")
        return True

    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
