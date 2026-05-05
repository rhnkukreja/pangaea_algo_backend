from datetime import date as _date
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from schemas.company import CompanyDetails
from pydantic import BaseModel
from typing import List
import os
import base64
import smtplib
from email.message import EmailMessage
from fastapi import APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv
import time
import traceback

load_dotenv()

router = APIRouter()

# Point to the new templates directory
templates = Jinja2Templates(directory="templates")

class EmailAgreementRequest(BaseModel):
    emails: List[str]
    pdf_base64: str

# Helper function that runs in the background
import smtplib
from email.message import EmailMessage
import os
import sys

def send_email_background_task(emails: List[str], pdf_bytes: bytes):
    print(f"--> [DEBUG 1] Background task actually started for emails: {emails}", flush=True)
    try:
        sender_email = os.getenv("SMTP_USER")
        sender_password = os.getenv("SMTP_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        
        # Safely parse the port to avoid silent crashes if Render parses it as a string with spaces
        raw_port = os.getenv("SMTP_PORT", 587)
        try:
            smtp_port = int(raw_port)
        except ValueError:
            print(f"--> [ERROR] Invalid SMTP_PORT value: '{raw_port}'. Defaulting to 587", flush=True)
            smtp_port = 587

        print(f"--> [DEBUG 2] Loaded ENV Vars - USER: {sender_email}, SERVER: {smtp_server}, PORT: {smtp_port}, HAS_PASSWORD: {bool(sender_password)}", flush=True)

        if not sender_email or not sender_password:
            print("--> [FATAL ERROR] SMTP credentials are not configured or missing.", flush=True)
            return

        print("--> [DEBUG 3] Building email message...", flush=True)
        msg = EmailMessage()
        msg['Subject'] = "Your Pangaea Developer Agreement"
        msg['From'] = sender_email
        msg['To'] = ", ".join(emails)
        msg.set_content(
            "Hello,\n\n"
            "Please find attached your generated Pangaea Developer Agreement.\n\n"
            "Best regards,\n"
            "The Pangaea Advisory Team"
        )

        msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename='Pangaea_Agreement.pdf')
        print(f"--> [DEBUG 4] Message built. PDF size: {len(pdf_bytes)} bytes. Attempting SMTP connection...", flush=True)

        # Automatically handle port 465 (SSL) vs 587 (TLS)
        if smtp_port == 465:
            print("--> [DEBUG 5] Connecting via SMTP_SSL (Port 465)...", flush=True)
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                print("--> [DEBUG 6] Connected to SSL server. Logging in...", flush=True)
                server.login(sender_email, sender_password)
                print("--> [DEBUG 7] Logged in successfully! Sending message...", flush=True)
                server.send_message(msg)
        else:
            print(f"--> [DEBUG 5] Connecting via standard SMTP (Port {smtp_port})...", flush=True)
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                print("--> [DEBUG 6] Connected to standard server. Initiating STARTTLS...", flush=True)
                server.starttls()
                print("--> [DEBUG 7] TLS secured. Logging in...", flush=True)
                server.login(sender_email, sender_password)
                print("--> [DEBUG 8] Logged in successfully! Sending message...", flush=True)
                server.send_message(msg)
            
        print(f"--> [SUCCESS] Email successfully sent to {emails}!", flush=True)
        
    except Exception as e:
        # flush=True forces the error to show up immediately in Render's log stream
        print(f"--> [EXCEPTION CAUGHT] Background Task Failed: {e}", flush=True)
        # This will print the EXACT line number that crashed
        traceback.print_exc() 
        sys.stdout.flush()

@router.post("/send-agreement-email")
async def send_agreement_email(request: EmailAgreementRequest, background_tasks: BackgroundTasks):
    if not request.emails:
        raise HTTPException(status_code=400, detail="No email addresses provided")
    
    try:
        t1 = time.time()
        # 1. Decode the base64 PDF (This is extremely fast, takes milliseconds)
        if "," in request.pdf_base64:
            _, encoded_data = request.pdf_base64.split(",", 1)
        else:
            encoded_data = request.pdf_base64
            
        pdf_bytes = base64.b64decode(encoded_data)
        
        # 2. Hand off the heavy 10-second SMTP work to a background thread
        background_tasks.add_task(send_email_background_task, request.emails, pdf_bytes)

        # 3. Return immediately to the frontend!
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
