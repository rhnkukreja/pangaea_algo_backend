from pydantic import BaseModel

class CompanyDetails(BaseModel):
    company_name: str
    company_address: str
    representative_name: str
    registration_number: str


    