import os
from fastapi import APIRouter, HTTPException
from supabase import Client
from client.supabase import get_supabase_client

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