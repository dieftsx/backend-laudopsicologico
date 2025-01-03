import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config.settings import settings

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USER
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False