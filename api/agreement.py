from datetime import date as _date
from fastapi.templating import Jinja2Templates
from schemas.company import CompanyDetails
from pydantic import BaseModel
from typing import List
import os
import base64
from fastapi import APIRouter, HTTPException, BackgroundTasks
import time
import traceback
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Point to the new templates directory
templates = Jinja2Templates(directory="templates")

class EmailAgreementRequest(BaseModel):
    emails: List[str]
    pdf_url: str

# Helper function that runs in the background
# Helper function that runs in the background
def send_email_background_task(emails: List[str], pdf_url: str):
    print(f"--> [DEBUG] Starting Brevo API email task for: {emails}", flush=True)
    try:
        # Get credentials from environment
        api_key = os.getenv("BREVO_API_KEY")
        sender_email = os.getenv("SMTP_USER") # Ensure this is your verified Gmail address!

        print(f"--> [DEBUG] SENDER EMAIL LOADED FROM ENV: '{sender_email}'", flush=True)

        if not api_key or not sender_email:
            print("--> [ERROR] BREVO_API_KEY or SMTP_USER is missing from environment variables.", flush=True)
            return

        # Build the headers Brevo expects
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

        # Format the recipient list for Brevo: [{"email": "user1@example.com"}, ...]
        to_list = [{"email": email} for email in emails]

        # Build the email payload
        payload = {
            "sender": {"name": "Pangaea Advisory Team", "email": sender_email},
            "to": to_list,
            "subject": "Your Pangaea Developer Agreement",
            "htmlContent": f"<p>Hello,</p><p>Your Pangaea Developer Agreement is ready.</p><p><a href='{pdf_url}'>Click here to download your agreement PDF</a></p><p>Best regards,<br>The Pangaea Advisory Team</p>"
        }

        # Fire the HTTP request (Port 443 - Bypasses Render Firewall completely!)
        print("--> [DEBUG] Sending request to Brevo...", flush=True)
        response = requests.post("https://api.brevo.com/v3/smtp/email", headers=headers, json=payload)

        # Check if it worked
        if response.status_code in [200, 201, 202]:
            print(f"--> [SUCCESS] Email sent successfully via Brevo! Response: {response.json()}", flush=True)
        else:
            print(f"--> [BREVO API ERROR] Status: {response.status_code}, Details: {response.text}", flush=True)

    except Exception as e:
        print(f"--> [EXCEPTION CAUGHT] API Email Failed: {e}", flush=True)
        traceback.print_exc()

@router.post("/send-agreement-email")
async def send_agreement_email(request: EmailAgreementRequest, background_tasks: BackgroundTasks):
    if not request.emails:
        raise HTTPException(status_code=400, detail="No email addresses provided")
    
    try:
        t1 = time.time()
        
        background_tasks.add_task(send_email_background_task, request.emails, request.pdf_url)

        # Return immediately to the frontend
        t2 = time.time()
        t3 = t2 - t1
        print(f"time taken to send the email is {t3}.")
        return {"success": True, "message": "Email queued for sending successfully."}
        
    except Exception as e:
        print(f"Email Payload Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process email: {str(e)}")

@router.post("/generate-agreement")
async def generate_agreement(company: CompanyDetails):
    # Load the template from the file
    template = templates.get_template("agreement_template.html")

    # Auto-generate date if not provided by the caller
    resolved_date = company.date if company.date else _date.today().strftime("%d %B %Y")
    
    # Render the HTML string
    html_content = template.render(
    company_name=company.company_name,
    company_address=company.company_address,
    representative_name=company.representative_name,
    registration_number=company.registration_number,

    designation=company.designation,
    date=resolved_date,

    platform_name="Pangaea",
    version="1.2",

    acceptance_items=[
        "I have read and understood these Terms.",
        "I confirm all information provided is accurate and compliant.",
        "I acknowledge Pangaea as the originating channel for registered clients.",
        "I agree that such clients will be routed through Pangaea.",
        "I acknowledge that commercial and registration terms may be governed by separately executed documents.",
        "I confirm I am authorised to accept these Terms on behalf of the Developer.",
    ]
)
    
    return {"html": html_content}
