from __future__ import annotations

import os
import secrets
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Request
from supabase import Client

from client.supabase import get_supabase_client
from schemas.referral import ReferralCreateResponse, ReferralTrackRequest, ReferralTrackResponse

router = APIRouter()

supabase: Client = get_supabase_client()


def _generate_referral_code() -> str:
    """
    Generate an 8-char, URL-safe *alphanumeric* code.

    Note: `secrets.token_urlsafe(6)` may include '-' and '_' so we strip those
    out and retry until we have enough alphanumerics.
    """
    while True:
        candidate = secrets.token_urlsafe(6)
        candidate = "".join(ch for ch in candidate if ch.isalnum())
        if len(candidate) >= 8:
            return candidate[:8]


def _get_resp_error(response: Any) -> Optional[Any]:
    # supabase-py response objects commonly expose `.error`; keep this resilient.
    return getattr(response, "error", None) or getattr(response, "errors", None)


@router.post("/generate", response_model=ReferralCreateResponse)
async def generate_referral_link(request: Request) -> ReferralCreateResponse:
    try:
        supabase = get_supabase_client()
        site_url = os.getenv("SITE_URL", "").rstrip("/")
        if not site_url:
            # Prefer the caller Origin (works behind proxies / different FE domains).
            origin = request.headers.get("origin")
            if origin:
                site_url = origin.rstrip("/")
            else:
                site_url = str(request.base_url).rstrip("/")
        if not site_url:
            site_url = "http://localhost:8080"

        last_error: Optional[Any] = None
        for _ in range(10):
            code = _generate_referral_code()
            response = supabase.table("referrals").insert({"code": code, "visit_count": 0}).execute()
            err = _get_resp_error(response)
            data = getattr(response, "data", None)
            if err:
                last_error = err
                continue
            if data:
                return ReferralCreateResponse(code=code, referral_url=f"{site_url}/contact?ref={code}")

        raise HTTPException(status_code=500, detail=f"Failed to generate unique referral code: {last_error}")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/track", response_model=ReferralTrackResponse)
async def track_referral_visit(payload: ReferralTrackRequest) -> ReferralTrackResponse:
    try:
        supabase = get_supabase_client()

        lookup = supabase.table("referrals").select("code, visit_count").eq("code", payload.code).execute()
        rows = getattr(lookup, "data", []) or []
        if not rows:
            raise HTTPException(status_code=404, detail="Referral code not found.")

        current = rows[0]
        current_count = int(current.get("visit_count") or 0)
        next_count = current_count + 1

        updated = (
            supabase.table("referrals")
            .update({"visit_count": next_count})
            .eq("code", payload.code)
            .execute()
        )
        updated_rows = getattr(updated, "data", []) or []
        if not updated_rows:
            raise HTTPException(status_code=500, detail="Failed to update referral visit count.")

        return ReferralTrackResponse(code=updated_rows[0]["code"], visit_count=int(updated_rows[0]["visit_count"] or 0))
    except HTTPException:
        raise
    except Exception as exc:
        print(f"TRACK ERROR: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
