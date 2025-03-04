import os
from supabase import create_client, Client

# Read Supabase URL and API Key from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Authentication functions
def sign_up(email, password, full_name=None, phone_number=None):
    """Register a new user with email and password"""
    try:
        # Sign up the user
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        # If sign up successful, create user profile
        if 'user' in response and response['user'] and 'id' in response['user']:
            user_id = response['user']['id']
            create_user_profile(user_id, full_name, phone_number)
            
        return response
    except Exception as e:
        return {"error": str(e)}

def sign_up_with_google():
    """Get Google OAuth sign up URL"""
    try:
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google"
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

# User profile functions
def create_user_profile(user_id, full_name=None, phone_number=None):
    """Create a new user profile"""
    try:
        response = supabase.table('user_profiles').insert({
            'id': user_id,
            'full_name': full_name,
            'phone_number': phone_number,
            'role': 'user',
            'subscription_plan': 'free'
        }).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def get_user_profile(user_id):
    """Get a user profile by user ID"""
    try:
        response = supabase.table('user_profiles').select('*').eq('id', user_id).execute()
        if response.data and len(response.data) > 0:
            print(f"User profile: {response.data[0]}")
            return response.data[0]
        return None
    except Exception as e:
        return {"error": str(e)}

def update_user_profile(user_id, data):
    """Update a user profile"""
    try:
        response = supabase.table('user_profiles').update(data).eq('id', user_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def verify_phone(user_id, phone_number):
    """Mark a phone number as verified"""
    try:
        response = supabase.table('user_profiles').update({
            'phone_number': phone_number,
            'phone_verified': True
        }).eq('id', user_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def update_subscription_plan(user_id, plan):
    """Update a user's subscription plan"""
    try:
        response = supabase.table('user_profiles').update({
            'subscription_plan': plan
        }).eq('id', user_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

# Topic functions
def get_topics(user_id=None, include_predefined=True):
    """Get all topics or user's subscribed topics"""
    try:
        if user_id:
            # Get user's subscribed topics
            response = supabase.table('topics').select(
                'id, name, description, is_predefined'
            ).eq('user_topics.user_id', user_id).execute()
            return response.data
        elif include_predefined:
            # Get all predefined topics
            response = supabase.table('topics').select('*').eq('is_predefined', True).execute()
            return response.data
        else:
            # Get all topics
            response = supabase.table('topics').select('*').execute()
            return response.data
    except Exception as e:
        return {"error": str(e)}

def create_topic(name, description="", is_predefined=False):
    """Create a new topic"""
    try:
        response = supabase.table('topics').insert({
            'name': name,
            'description': description,
            'is_predefined': is_predefined
        }).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def update_topic(topic_id, data):
    """Update a topic"""
    try:
        response = supabase.table('topics').update(data).eq('id', topic_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def delete_topic(topic_id):
    """Delete a topic"""
    try:
        response = supabase.table('topics').delete().eq('id', topic_id).execute()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

# User topic subscription functions
def subscribe_to_topic(user_id, topic_id):
    """Subscribe a user to a topic"""
    try:
        response = supabase.table('user_topics').insert({
            'user_id': user_id,
            'topic_id': topic_id
        }).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def unsubscribe_from_topic(user_id, topic_id):
    """Unsubscribe a user from a topic"""
    try:
        response = supabase.table('user_topics').delete().eq('user_id', user_id).eq('topic_id', topic_id).execute()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def get_user_topics(user_id):
    """Get all topics a user is subscribed to"""
    try:
        response = supabase.table('user_topics').select(
            'topics:topic_id(id, name, description, is_predefined)'
        ).eq('user_id', user_id).execute()
        
        # Extract the topics from the response
        topics = []
        for item in response.data:
            if 'topics' in item and item['topics']:
                topics.append(item['topics'])
        
        return topics
    except Exception as e:
        return {"error": str(e)}

# Newsletter functions
def get_newsletters(user_id=None, topic_id=None):
    """Get newsletters for a user or topic"""
    try:
        query = supabase.table('newsletters').select('*')
        
        if topic_id:
            query = query.eq('topic_id', topic_id)
        
        response = query.order('created_at', desc=True).execute()
        
        # If user_id is provided, filter newsletters for subscribed topics
        if user_id and not topic_id:
            user_topics = get_user_topics(user_id)
            if isinstance(user_topics, list):
                topic_ids = [topic['id'] for topic in user_topics]
                filtered_newsletters = [n for n in response.data if n['topic_id'] in topic_ids]
                return filtered_newsletters
        
        return response.data
    except Exception as e:
        return {"error": str(e)}

def create_newsletter(user_id, title, content, topic_id):
    """Create a new newsletter"""
    try:
        response = supabase.table('newsletters').insert({
            'user_id': user_id,
            'title': title,
            'content': content,
            'topic_id': topic_id
        }).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def update_newsletter(newsletter_id, data):
    """Update a newsletter"""
    try:
        response = supabase.table('newsletters').update(data).eq('id', newsletter_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def delete_newsletter(newsletter_id):
    """Delete a newsletter"""
    try:
        response = supabase.table('newsletters').delete().eq('id', newsletter_id).execute()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

# Chat message functions
def get_chat_messages(user_id):
    """Get all chat messages for a user"""
    try:
        response = supabase.table('chat_messages').select('*').eq('user_id', user_id).order('created_at', desc=False).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def create_chat_message(user_id, content, is_from_user=True):
    """Create a new chat message"""
    try:
        response = supabase.table('chat_messages').insert({
            'user_id': user_id,
            'content': content,
            'is_from_user': is_from_user
        }).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

# Todo functions
def get_todos(user_id):
    """Get all todos for a user"""
    try:
        response = supabase.table('todos').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def create_todo(user_id, title, description=""):
    """Create a new todo"""
    try:
        response = supabase.table('todos').insert({
            'user_id': user_id,
            'title': title,
            'description': description,
            'completed': False
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

# Admin functions
def get_all_users():
    """Get all users (admin only)"""
    try:
        response = supabase.table('user_profiles').select('*').execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def set_user_role(user_id, role):
    """Set a user's role (admin only)"""
    try:
        response = supabase.table('user_profiles').update({
            'role': role
        }).eq('id', user_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def get_all_newsletters():
    """Get all newsletters (admin only)"""
    try:
        response = supabase.table('newsletters').select('*, topics:topic_id(name)').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}