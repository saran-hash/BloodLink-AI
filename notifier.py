import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class Notifier:
    def send_notification(self, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

class EmailNotifier(Notifier):
    def send_notification(self, to_email, donor_name, patient_name, blood_group, hospital, contact_number):
        sender_email = "saransivakumar20@gmail.com"
        app_password = "rhhyxlhxkichunxp"

        subject = "Urgent Blood Request"
        body = f"""
        Dear {donor_name},

        🚨 An urgent blood donation is needed for patient {patient_name}.
        Blood Group: {blood_group}
        Hospital: {hospital}
        Contact Number: {contact_number}

        If you're eligible and available, please consider donating.

        Thank you!
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            server.quit()
            print(f" Email sent to {to_email}")
        except Exception as e:
            print(f" Email failed to {to_email}: {e}")

class WhatsAppNotifier(Notifier):
    def send_notification(self, phone, message):
        instance_id = os.getenv("ULTRAMSG_INSTANCE_ID")
        token = os.getenv("ULTRAMSG_TOKEN")

        url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
        payload = {
            "token": token,
            "to": phone,
            "body": message,
            "priority": 10
        }

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print(f" WhatsApp sent to {phone}")
            else:
                print(f" Failed to send. Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f" Error: {e}")
