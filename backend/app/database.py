from supabase import create_client, Client
from app.config import settings

# Initialize Supabase client using URL and Service Role Key (to bypass RLS for admin actions)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_supabase() -> Client:
    """
    Returns the initialized Supabase client instance.
    """
    return supabase
