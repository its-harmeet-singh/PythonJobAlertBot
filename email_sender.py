import os
from dotenv import load_dotenv
from courier.client import Courier
import courier

load_dotenv()

COURIER_AUTH_TOKEN = os.getenv("COURIER_AUTH_TOKEN")
COURIER_EMAIL_TO = os.getenv("COURIER_EMAIL_TO")
COURIER_TEMPLATE_ID = os.getenv("COURIER_TEMPLATE_ID")

client = Courier(authorization_token=COURIER_AUTH_TOKEN)

def send_job_template_email(recipient_name: str, jobs: list, date: str):
    response = client.send(
        message={
            "to": {
                "email": COURIER_EMAIL_TO,
            },
            "template": COURIER_TEMPLATE_ID,
            "data": {
                "name": recipient_name,
                "jobs": jobs,
                "date": date
            },
            "routing": {
                "method": "single",
                "channels": ["email"]
            }
        }
    )

    print("📧 Courier Email Sent | Request ID:", response)