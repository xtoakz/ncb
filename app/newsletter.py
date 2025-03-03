from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.auth import login_required
import supabase_client as supabase

bp = Blueprint('newsletter', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user', {}).get('id')
    
    # Get user profile
    user_profile = supabase.get_user_profile(user_id)
    
    # Get user's subscribed topics
    user_topics = supabase.get_user_topics(user_id)
    
    # Get newsletters for user's subscribed topics
    newsletters = supabase.get_newsletters(user_id)
    
    # Get chat messages
    chat_messages = supabase.get_chat_messages(user_id)
    
    if isinstance(user_topics, dict) and 'error' in user_topics:
        flash(f'Error fetching topics: {user_topics["error"]}', 'danger')
        user_topics = []
    
    if isinstance(newsletters, dict) and 'error' in newsletters:
        flash(f'Error fetching newsletters: {newsletters["error"]}', 'danger')
        newsletters = []
    
    if isinstance(chat_messages, dict) and 'error' in chat_messages:
        flash(f'Error fetching chat messages: {chat_messages["error"]}', 'danger')
        chat_messages = []
    
    return render_template('newsletter/dashboard.html',
                              user_profile=user_profile,
                              topics=user_topics,
                              newsletters=newsletters,
                              chat_messages=chat_messages,
                              supabase=supabase)

@bp.route('/chat', methods=['POST'])
@login_required
def chat():
    user_id = session.get('user', {}).get('id')
    message = request.form.get('message')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Save user message
    user_message = supabase.create_chat_message(user_id, message, is_from_user=True)
    
    if isinstance(user_message, dict) and 'error' in user_message:
        return jsonify({'error': f'Error saving message: {user_message["error"]}'}), 500
    
    # Generate a response (in a real app, this would be an AI response)
    # For this example, we'll just echo the message back with some context
    response_text = f"I received your message: '{message}'. This is a simulated response from the NewsletterChat AI."
    
    # Save system response
    system_message = supabase.create_chat_message(user_id, response_text, is_from_user=False)
    
    if isinstance(system_message, dict) and 'error' in system_message:
        return jsonify({'error': f'Error saving response: {system_message["error"]}'}), 500
    
    # Return both messages
    return jsonify({
        'user_message': {
            'content': message,
            'is_from_user': True,
            'created_at': user_message[0]['created_at'] if isinstance(user_message, list) and len(user_message) > 0 else None
        },
        'system_message': {
            'content': response_text,
            'is_from_user': False,
            'created_at': system_message[0]['created_at'] if isinstance(system_message, list) and len(system_message) > 0 else None
        }
    })

@bp.route('/get-news', methods=['POST'])
@login_required
def get_news():
    topic = request.json.get('topic')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    # In a real app, this would fetch real news data from an API
    # For this example, we'll return mock data
    mock_data = {
        'results': [
            {
                'title': f'Latest news about {topic}',
                'description': f'This is a sample news article about {topic}.',
                'url': 'https://example.com/news/1',
                'snippets': f'Sample excerpt from an article about {topic}...'
            },
            {
                'title': f'Breaking: New developments in {topic}',
                'description': f'Another sample news article about {topic}.',
                'url': 'https://example.com/news/2',
                'snippets': f'More sample content about {topic}...'
            }
        ],
        'qnas': [
            {
                'question': f'What is the latest trend in {topic}?',
                'answer': f'The latest trend in {topic} is the increasing focus on digital transformation and AI integration.'
            },
            {
                'question': f'Who are the key players in {topic}?',
                'answer': f'The key players in {topic} include major corporations and innovative startups that are pushing the boundaries.'
            }
        ],
        'videos': [
            {
                'title': f'Video guide to {topic}',
                'description': f'A comprehensive video about {topic}',
                'src': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': f'Expert interview on {topic}',
                'description': f'Industry experts discuss the future of {topic}',
                'src': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            }
        ],
        'related': [
            f'{topic} trends',
            f'{topic} news',
            f'{topic} analysis',
            f'{topic} future',
            f'{topic} technology'
        ]
    }
    
    return jsonify(mock_data)

@bp.route('/topics')
@login_required
def topics():
    user_id = session.get('user', {}).get('id')
    
    # Get user profile to check subscription plan
    user_profile = supabase.get_user_profile(user_id)
    
    # Get all available topics
    all_topics = supabase.get_topics()
    
    # Get user's subscribed topics
    user_topics = supabase.get_user_topics(user_id)
    
    if isinstance(all_topics, dict) and 'error' in all_topics:
        flash(f'Error fetching topics: {all_topics["error"]}', 'danger')
        all_topics = []
    
    if isinstance(user_topics, dict) and 'error' in user_topics:
        flash(f'Error fetching subscribed topics: {user_topics["error"]}', 'danger')
        user_topics = []
    
    # Convert user_topics to a list of IDs for easy checking
    subscribed_topic_ids = [topic['id'] for topic in user_topics] if isinstance(user_topics, list) else []
    
    return render_template('newsletter/topics.html',
                          all_topics=all_topics,
                          subscribed_topic_ids=subscribed_topic_ids,
                          user_profile=user_profile,
                          supabase=supabase)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    user_id = session.get('user', {}).get('id')
    title = request.form.get('title')
    content = request.form.get('content')
    topic_id = request.form.get('topic')
    
    if not title or not content or not topic_id:
        flash('All fields are required', 'danger')
        return redirect(url_for('newsletter.dashboard'))
    
    # Process the data (save to database, etc.)
    result = supabase.create_newsletter(user_id, title, content, topic_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error creating newsletter: {result["error"]}', 'danger')
    else:
        flash('Newsletter created successfully!', 'success')
    
    return redirect(url_for('newsletter.dashboard'))

@bp.route('/create-topic', methods=['POST'])
@login_required
def create_topic():
    user_id = session.get('user', {}).get('id')
    
    # Get user profile to check subscription plan
    user_profile = supabase.get_user_profile(user_id)
    
    # Only premium users can create custom topics
    if not user_profile or user_profile.get('subscription_plan') != 'premium':
        flash('Only premium users can create custom topics', 'danger')
        return redirect(url_for('newsletter.topics'))
    
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        flash('Topic name is required', 'danger')
        return redirect(url_for('newsletter.topics'))
    
    # Create the topic
    result = supabase.create_topic(name, description, is_predefined=False)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error creating topic: {result["error"]}', 'danger')
    else:
        # Subscribe the user to the new topic
        topic_id = result[0]['id'] if isinstance(result, list) and len(result) > 0 else None
        if topic_id:
            supabase.subscribe_to_topic(user_id, topic_id)
            flash('Topic created and subscribed successfully!', 'success')
        else:
            flash('Topic created but could not subscribe automatically', 'warning')
    
    
    return redirect(url_for('newsletter.topics'))

@bp.route('/update_topic/<topic_id>', methods=['POST'])
@login_required
def update_topic(topic_id):
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        flash('Topic name is required', 'danger')
        return redirect(url_for('newsletter.topics'))
    
    result = supabase.update_topic(topic_id, {'name': name, 'description': description})
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error updating topic: {result["error"]}', 'danger')
    else:
        flash('Topic updated successfully!', 'success')
    
    return redirect(url_for('newsletter.topics'))

@bp.route('/delete_topic/<topic_id>', methods=['POST'])
@login_required
def delete_topic(topic_id):
    result = supabase.delete_topic(topic_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error deleting topic: {result["error"]}', 'danger')
    else:
        flash('Topic deleted successfully!', 'success')
    
    return redirect(url_for('newsletter.topics'))