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

# Newsletter operations
def get_newsletters(user_id):
    """Get all newsletters for a user"""
    try:
        response = supabase.table('newsletters').select('*').eq('user_id', user_id).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

def create_newsletter(user_id, title, content="", delivery_platform="whatsapp"):
    """Create a new newsletter for a user"""
    try:
        response = supabase.table('newsletters').insert({
            'user_id': user_id,
            'title': title,
            'content': content,
            'delivery_platform': delivery_platform,
            'status': 'draft'
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

def send_newsletter(newsletter_id):
    """Send a newsletter"""
    try:
        # First, get the newsletter
        response = supabase.table('newsletters').select('*').eq('id', newsletter_id).execute()
        if not response.data:
            return {"error": "Newsletter not found"}
        
        newsletter = response.data[0]
        
        # Update the status to 'sent'
        update_response = supabase.table('newsletters').update({
            'status': 'sent',
            'sent_at': 'now()'
        }).eq('id', newsletter_id).execute()
        
        # In a real application, you would integrate with WhatsApp/Telegram/Email APIs here
        # For now, we'll just return success
        return {"success": True, "message": f"Newsletter sent via {newsletter['delivery_platform']}"}
    except Exception as e:
        return {"error": str(e)}

def get_news(topic):
    """Get news articles based on a topic"""
    try:
        # In a real application, you would integrate with a news API here
        # For now, we'll return mock data
        import datetime
        current_date = datetime.datetime.now().strftime('%d.%m.%Y')
        
        mock_data = {
            "results": [
                {
                    "title": f"Latest news about {topic}",
                    "description": f"This is a sample description about {topic}.",
                    "snippets": f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Topics related to {topic} are trending today.",
                    "url": "https://example.com/news/1",
                    "source": "example.com"
                },
                {
                    "title": f"Breaking: New developments in {topic}",
                    "description": f"Recent updates about {topic} that you should know.",
                    "snippets": f"More information about {topic} is expected to be released soon.",
                    "url": "https://example.com/news/2",
                    "source": "example.com"
                },
                {
                    "title": f"Analysis: What {topic} means for the future",
                    "description": f"Experts weigh in on the implications of {topic}.",
                    "snippets": f"Experts believe that {topic} will have significant impact on various sectors.",
                    "url": "https://example.com/news/3",
                    "source": "example.com"
                }
            ],
            "qnas": [
                {
                    "question": f"What is the latest news about {topic}?",
                    "answer": f"The latest news about {topic} involves new developments and research findings."
                },
                {
                    "question": f"Why is {topic} important?",
                    "answer": f"{topic} is important because it affects multiple aspects of daily life."
                }
            ]
        }
        
        return mock_data
    except Exception as e:
        return {"error": str(e)}