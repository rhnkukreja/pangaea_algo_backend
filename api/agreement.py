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

load_dotenv()

router = APIRouter()

# Point to the new templates directory
templates = Jinja2Templates(directory="templates")

class EmailAgreementRequest(BaseModel):
    emails: List[str]
    pdf_base64: str

# Helper function that runs in the background
def send_email_background_task(emails: List[str], pdf_bytes: bytes):
    try:
        # Get SMTP credentials from environment variables
        sender_email = os.getenv("SMTP_USER")
        sender_password = os.getenv("SMTP_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))

        if not sender_email or not sender_password:
            print("Email Error: SMTP credentials are not configured on the server.")
            return

        # Create the email message
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

        # Attach the PDF
        msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename='Pangaea_Agreement.pdf')

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        print(f"Background task: Email successfully sent to {emails}")
        
    except Exception as e:
        print(f"Background Task Email Error: {e}")

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
