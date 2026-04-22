import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_SECRET_KEY")  # public anon key OR service key

def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_API_KEY:
        raise ValueError("Missing Supabase environment variables")

    return create_client(SUPABASE_URL, SUPABASE_API_KEY)


# Optional: singleton (recommended for apps)
supabase: Client = get_supabase_client()

