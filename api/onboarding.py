from __future__ import annotations

import os
import time
import uuid
from typing import Any, Optional
from urllib.parse import quote

import boto3
from botocore.client import Config
from fastapi import APIRouter, Depends, Header, HTTPException
from client.supabase import supabase
from schemas.onboarding import ProfileSubmitRequest, ProjectSubmitRequest, PresignRequest, CompanyPayload, ProjectPayload, FileMeta, UploadEnvelope

router = APIRouter()

BUCKET_NAME = os.getenv("S_BUCKET_NAME", "pangea")
S_ACCESS_KEY = os.getenv("S_ACCESS_KEY")
S_SECRET_ACCESS_KEY = os.getenv("S_SECRET_ACCESS_KEY")
S_ENDPOINT = os.getenv("S_ENDPOINT")
S_REGION = os.getenv("S_REGION", "ap-northeast-2")
SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")


def require_storage_env() -> None:
    if not all([S_ACCESS_KEY, S_SECRET_ACCESS_KEY, S_ENDPOINT]):
        raise HTTPException(status_code=500, detail="Missing S3 storage environment variables.")


def get_s3_client():
    require_storage_env()
    return boto3.client(
        "s3",
        endpoint_url=S_ENDPOINT,
        region_name=S_REGION,
        aws_access_key_id=S_ACCESS_KEY,
        aws_secret_access_key=S_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
    )


def build_public_url(object_key: str) -> str:
    if SUPABASE_URL:
        return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{quote(object_key)}"
    if S_ENDPOINT:
        return f"{S_ENDPOINT.rstrip('/')}/{BUCKET_NAME}/{quote(object_key)}"
    raise HTTPException(status_code=500, detail="Unable to build public storage URL.")


def sanitize_filename(file_name: str) -> str:
    return "".join(char if char.isalnum() or char in {".", "-", "_"} else "-" for char in file_name)


def verify_bearer_token(authorization: Optional[str] = Header(default=None)) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token.")

    token = authorization.removeprefix("Bearer ").strip()
    try:
        response = supabase.auth.get_user(token)
        user = getattr(response, "user", None)
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Invalid auth token: {exc}") from exc

    if not user:
        raise HTTPException(status_code=401, detail="Unable to resolve authenticated user.")

    return {
        "id": user.id,
        "email": getattr(user, "email", None),
        "user_metadata": getattr(user, "user_metadata", {}) or {},
        "app_metadata": getattr(user, "app_metadata", {}) or {},
    }


def get_meta_value(item: Any, field: str) -> Optional[str]:
    if not item:
        return None
    if isinstance(item, dict):
        return item.get(field)
    return getattr(item, field, None)


@router.post("/storage/presign")
def create_presigned_upload(payload: PresignRequest, user=Depends(verify_bearer_token)):
    safe_name = sanitize_filename(payload.file_name)
    object_key = f"{user['id']}/{payload.category}/{int(time.time())}-{uuid.uuid4().hex[:8]}-{safe_name}"

    s3_client = get_s3_client()
    upload_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": object_key,
            "ContentType": payload.content_type,
        },
        ExpiresIn=900,
    )

    return {
        "upload_url": upload_url,
        "public_url": build_public_url(object_key),
        "object_key": object_key,
        "headers": {
            "Content-Type": payload.content_type,
        },
    }


@router.get("/me")
def get_my_onboarding_state(user=Depends(verify_bearer_token)):
    # FIXED: Removed .maybe_single() to prevent AttributeError on 0 rows
    profile_response = (
        supabase.table("developers")
        .select("*")
        .eq("auth_user_id", user["id"])
        .execute()
    )
    
    # Safely extract data list, default to empty list if none
    profile_data = getattr(profile_response, "data", [])

    if not profile_data:
        raise HTTPException(status_code=404, detail="Developer profile not found.")
        
    profile = profile_data[0]

    projects_response = (
        supabase.table("projects")
        .select("*")
        .eq("developer_id", profile["id"])
        .order("created_at", desc=True)
        .execute()
    )
    
    projects_data = getattr(projects_response, "data", [])

    return {
        "auth_user_id": user["id"],
        "company_name": profile.get("company_name", ""),
        "signed_agreement_url": profile.get("signed_agreement_url"),
        "registration_certificate_url": profile.get("registration_cert_url"),
        "project_portfolio_url": profile.get("project_portfolio_url"),
        "financial_statements_url": profile.get("financial_statements_url"),
        "company": profile,
        "projects": projects_data,
    }


@router.post("/profile")
def submit_profile(payload: ProfileSubmitRequest, user=Depends(verify_bearer_token)):
    company_documents = payload.uploads.companyDocuments or {}
    agreement = payload.uploads.agreement or {}

    row = {
        "auth_user_id": user["id"],
        "company_name": payload.company.companyName,
        "headquarters": payload.company.headquarters,
        "years_in_operation": payload.company.yearsInOperation or None,
        "completed_projects": payload.company.completedProjects or None,
        "key_markets": payload.company.keyMarkets,
        "company_website": payload.company.companyWebsite or None,
        "partnerships": payload.company.partnerships or None,
        "units_sold": payload.company.unitsSold or None,
        "number_of_investors": payload.company.numberOfInvestors or None,
        "repeat_buyers_percent": payload.company.repeatBuyers or None,
        "buyer_types": payload.company.buyerTypes,
        "registration_cert_url": get_meta_value(company_documents.get("registrationCertificate"), "url"),
        "project_portfolio_url": get_meta_value(company_documents.get("projectPortfolio"), "url"),
        "financial_statements_url": get_meta_value(company_documents.get("financialStatements"), "url"),
        "signed_agreement_url": get_meta_value(agreement.get("signedAgreementPdf"), "url") or get_meta_value(agreement.get("signatureImage"), "url"),
    }

    # THE FIX: Manually check if the user already has a profile
    existing_profile = supabase.table("developers").select("id").eq("auth_user_id", user["id"]).execute()
    existing_data = getattr(existing_profile, "data", [])

    if existing_data:
        # If profile exists, UPDATE it using its specific ID
        profile_id = existing_data[0]["id"]
        result = supabase.table("developers").update(row).eq("id", profile_id).execute()
    else:
        # If no profile exists, INSERT a new one
        result = supabase.table("developers").insert(row).execute()

    result_data = getattr(result, "data", [])
    if not result_data:
        raise HTTPException(status_code=500, detail="Failed to save developer profile.")

    return {
        "success": True,
        "submission_id": result_data[0]["id"],
    }

@router.post("/projects")
def submit_project(payload: ProjectSubmitRequest, user=Depends(verify_bearer_token)):
    # FIXED: Safely fetch developer without .maybe_single()
    dev_response = supabase.table("developers").select("id").eq("auth_user_id", user["id"]).execute()
    dev_data = getattr(dev_response, "data", [])
    
    if not dev_data:
        raise HTTPException(status_code=400, detail="Developer profile must be completed before adding projects.")
    
    dev_id = dev_data[0]["id"]

    project_assets = payload.uploads.projectAssets or {}
    incoming_images = project_assets.get("projectImages") or payload.project.projectImages or []

    foreign_inv_allowed = None
    if payload.project.foreignInvestmentAllowed:
        foreign_inv_allowed = str(payload.project.foreignInvestmentAllowed).lower() in ['true', '1', 't', 'y', 'yes']

    row = {
        "developer_id": dev_id,
        "project_name": payload.project.projectName,
        "country": payload.project.country,
        "city": payload.project.city,
        "micro_location": payload.project.microLocation,
        "project_type": payload.project.projectType or None,
        "project_stage": payload.project.projectStage or None,
        "distance_to_airport_km": payload.project.distanceToAirport or None,
        "distance_to_business_district_km": payload.project.distanceToBusinessDistrict or None,
        "public_transport_access": payload.project.publicTransportAccess or None,
        "nearby_infrastructure": payload.project.nearbyInfrastructure or None,
        "area_type": payload.project.areaType or None,
        "currency": payload.project.currency or "USD",
        "min_ticket_size": payload.project.minTicketSize or None,
        "max_ticket_size": payload.project.maxTicketSize or None,
        "price_positioning": payload.project.pricePositioning or None,
        "expected_annual_returns_percent": payload.project.expectedAnnualReturns or None,
        "rental_yield_estimate_percent": payload.project.rentalYieldEstimate or None,
        "foreign_investment_allowed": foreign_inv_allowed,
        "ownership_structure": payload.project.ownershipStructure or None,
        "golden_visa_linked": payload.project.goldenVisa,
        "tax_considerations": payload.project.taxConsiderations or None,
        "legal_structure_notes": payload.project.legalStructureNotes or None,
        "expected_completion_date": payload.project.expectedCompletionDate or None,
        "total_units": payload.project.totalUnits or None,
        "units_available": payload.project.unitsAvailable or None,
        "developer_track_record": payload.project.developerTrackRecord or None,
        "project_images": [get_meta_value(item, "url") for item in incoming_images if get_meta_value(item, "url")] or None,
        "floor_plans_url": get_meta_value(project_assets.get("floorPlans") or payload.project.floorPlans, "url"),
        "brochure_url": get_meta_value(project_assets.get("brochure") or payload.project.brochure, "url"),
    }

    if payload.project_id:
        result = (
            supabase.table("projects")
            .update(row)
            .eq("id", payload.project_id)
            .eq("developer_id", dev_id)
            .execute()
        )
        result_data = getattr(result, "data", [])
        if not result_data:
            raise HTTPException(status_code=404, detail="Project not found for this user.")
        saved_id = result_data[0]["id"]
    else:
        row["id"] = str(uuid.uuid4())
        result = supabase.table("projects").insert(row).execute()
        result_data = getattr(result, "data", [])
        if not result_data:
            raise HTTPException(status_code=500, detail="Failed to create project.")
        saved_id = result_data[0]["id"]

    return {
        "success": True,
        "submission_id": saved_id,
    }