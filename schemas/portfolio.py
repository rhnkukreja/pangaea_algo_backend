from pydantic import BaseModel
from typing import List, Optional

class InvestorProfileRequest(BaseModel):
    max_budget: float
    visa_mandatory: bool
    geographic_preferences: List[str]  # e.g., ["GR", "PT", "AE", "TH"]
    primary_objective: str             # e.g., "Yield / Cash Flow", "Residency"
    usage_intent: str                  # e.g., "Pure investment", "Primary relocation"
    risk_appetite: str                 # e.g., "Conservative", "Opportunistic"
    property_types: List[str]          # e.g., ["Apartments", "Villas"]

    # --- Advisory / CRM Fields (Saved for context, but ignored by algorithm) ---
    timeline: Optional[str] = None             # Q3
    holding_period: Optional[str] = None       # Q4
    citizenship_interest: Optional[str] = None # Q6 (If separate from visa)
    ownership_type: Optional[str] = None       # Q7 (Freehold/Leasehold)
    family_composition: Optional[str] = None   # Q11
    experience_level: Optional[str] = None     # Q12
    # Add any remaining specific fields from Q14/Q15 here
    
    # Optional: A catch-all dictionary if you just want to dump the raw frontend JSON
    raw_survey_answers: Optional[dict] = None