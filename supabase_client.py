import os
from supabase import create_client, Client

# Read Supabase URL and API Key from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Authentication functions
def sign_up(email, password):
    """Register a new user with email and password"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        return {"error": str(e)}

def sign_in(email, password):
    """Sign in a user with email and password"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        return {"error": str(e)}

def sign_out(jwt):
    """Sign out a user"""
    try:
        supabase.auth.sign_out(jwt)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

# Todo operations
def get_todos(user_id):
    """Get all todos for a user"""
    try:
        response = supabase.table('todos').select('*').eq('user_id', user_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def create_todo(user_id, title, description="", completed=False):
    """Create a new todo for a user"""
    try:
        response = supabase.table('todos').insert({
            'user_id': user_id,
            'title': title,
            'description': description,
            'completed': completed
        }).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def update_todo(todo_id, data):
    """Update a todo"""
    try:
        response = supabase.table('todos').update(data).eq('id', todo_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def delete_todo(todo_id):
    """Delete a todo"""
    try:
        response = supabase.table('todos').delete().eq('id', todo_id).execute()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}