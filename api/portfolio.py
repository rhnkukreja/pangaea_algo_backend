import os
from fastapi import APIRouter, HTTPException
from supabase import Client
from client.supabase import get_supabase_client
from schemas.portfolio import InvestorProfileRequest

router = APIRouter()

supabase: Client = get_supabase_client()
    
@router.get("/developers")
async def get_developers():
    try:
        supabase = get_supabase_client()
        # Fetch all developers, ordered by newest first
        response = supabase.table("developers").select("*").order("created_at", desc=True).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects")
async def get_projects():
    try:
        supabase = get_supabase_client()
        # Fetch all projects and join the company_name from the parent developers table
        response = supabase.table("projects").select("*, developers(company_name)").order("created_at", desc=True).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/recommendations")
async def get_project_recommendations(profile: InvestorProfileRequest):
    try:
        supabase = get_supabase_client()
        
        # Fetch all projects and the developer company name
        response = supabase.table("projects").select("*, developers(company_name)").execute()
        all_projects = response.data

        if not all_projects:
            return {"data": []}

        eligible_projects = []
        
        # 1. HARD FILTER: Budget Knockout
        for project in all_projects:
            min_ticket = float(project.get("min_ticket_size") or 0)
            
            if min_ticket <= profile.max_budget:
                eligible_projects.append(project)

        # 2. SOFT FILTER: Scoring Logic
        scored_projects = []
        for p in eligible_projects:
            score = 0
            
            # Extract necessary fields
            country = p.get("country")
            project_type = p.get("project_type")
            project_stage = p.get("project_stage")
            golden_visa = p.get("golden_visa_linked")
            project_name = (p.get("project_name") or "").lower()
            unit_types = p.get("unit_types") or {}
            
            # A. Visa / Citizenship Status (High Weight: 30 Points)
            if profile.visa_mandatory and golden_visa is True:
                score += 30
                
            # B. Geographic Preference (High Weight: 30 Points)
            if country in profile.geographic_preferences:
                score += 30
                
            # C. Primary Objective & Usage Intent (Medium Weight: 20 Points)
            is_yield_focused = profile.primary_objective == "Yield / Cash Flow" or profile.usage_intent == "Pure investment"
            is_lifestyle_focused = profile.primary_objective in ["Primary Relocation", "Lifestyle"]
            
            if is_yield_focused:
                expected_returns_str = p.get("expected_annual_returns_percent")
                try:
                    expected_returns = float(expected_returns_str) if expected_returns_str else 0.0
                except ValueError:
                    expected_returns = 0.0
                    
                if expected_returns > 6.0 or project_type == "Mixed-use":
                    score += 20
            
            elif is_lifestyle_focused:
                if project_type == "Residential":
                    score += 20
                    
            # D. Risk Appetite (Low Weight: 10 Points)
            if profile.risk_appetite == "Conservative":
                # Assuming AE (UAE) as the proxy for high stability locations as per standard logic
                if project_stage == "Completed" or country == "AE":
                    score += 10
            elif profile.risk_appetite == "Opportunistic":
                if project_stage == "Under Construction":
                    score += 10
                    
            # E. Type of Property (Low Weight: 10 Points)
            # Flatten unit types keys to check against keywords
            unit_keys_str = " ".join(unit_types.keys()).lower()
            
            for pt in profile.property_types:
                # Remove trailing 's' for standard singular keyword matching (e.g., Apartments -> Apartment)
                keyword = pt.lower().rstrip('s')
                if keyword in project_name or keyword in unit_keys_str:
                    score += 10
                    break # Only apply the 10 points once if a match is found
            
            # Append score to project dictionary
            p["match_score"] = score
            scored_projects.append(p)
            
        # 3. Sort by highest match score descending
        scored_projects.sort(key=lambda x: x["match_score"], reverse=True)
        
        # 4. Return Top 10-12 Projects
        return {"data": scored_projects[:12]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))