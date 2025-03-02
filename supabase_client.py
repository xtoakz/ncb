import os
from supabase import create_client, Client

# Lese die Supabase-URL und den API-Key aus den Umgebungsvariablen
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Erstelle den Supabase-Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
