from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from schemas.company import CompanyDetails

router = APIRouter()

# Point to the new templates directory
templates = Jinja2Templates(directory="templates")

@router.post("/generate-agreement")
async def generate_agreement(company: CompanyDetails):
    # Load the template from the file
    template = templates.get_template("agreement_template.html")
    
    # Render the HTML string
    html_content = template.render(
        company_name=company.company_name,
        company_address=company.company_address,
        representative_name=company.representative_name,
        registration_number=company.registration_number
    )
    
    return {"html": html_content}