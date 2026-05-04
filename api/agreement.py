from datetime import date as _date

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from schemas.company import CompanyDetails

router = APIRouter()

# Point to the new templates directory
templates = Jinja2Templates(directory="templates")

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
