from pydantic import BaseModel


class ReferralCreateResponse(BaseModel):
    code: str
    referral_url: str


class ReferralTrackRequest(BaseModel):
    code: str


class ReferralTrackResponse(BaseModel):
    code: str
    visit_count: int

