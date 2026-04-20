from fastapi import APIRouter
from schemas.company import CompanyDetails
from jinja2 import Template

# Initialize the router
router = APIRouter()

# In a real app, this template might be loaded from a separate .html file
AGREEMENT_TEMPLATE = """
<div style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; color: #1f2937;">
    <h2 style="text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 24px;">AGREEMENT</h2>
    
    <p><strong>The parties:</strong></p>
    
    <p>
        <span style="text-transform: uppercase; font-weight: bold;">{{ company_name }}</span>,<br>
        having its head office and principal place of business at {{ company_address }},<br>
        registered under the number {{ registration_number }}, duly represented for the present Agreement by <strong>{{ representative_name }}</strong>.
    </p>
    </div>
"""

# Note: We don't include "/api" here. We handle that in main.py
@router.post("/generate-agreement")
async def generate_agreement(company: CompanyDetails):
    template = Template(AGREEMENT_TEMPLATE)
    
    html_content = template.render(
        company_name=company.company_name,
        company_address=company.company_address,
        representative_name=company.representative_name,
        registration_number=company.registration_number
    )
    
    return {"html": html_content}