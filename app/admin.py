from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.auth import admin_required
import supabase_client as supabase

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
@admin_required
def dashboard():
    # Get admin user info
    user_id = session.get('user', {}).get('id')
    user_profile = supabase.get_user_profile(user_id)
    
    # Get all users
    users = supabase.get_all_users()
    
    # Get all topics
    topics = supabase.get_topics(include_predefined=False)
    
    # Get all newsletters
    newsletters = supabase.get_all_newsletters()
    
    if isinstance(users, dict) and 'error' in users:
        flash(f'Error fetching users: {users["error"]}', 'danger')
        users = []
    
    if isinstance(topics, dict) and 'error' in topics:
        flash(f'Error fetching topics: {topics["error"]}', 'danger')
        topics = []
    
    if isinstance(newsletters, dict) and 'error' in newsletters:
        flash(f'Error fetching newsletters: {newsletters["error"]}', 'danger')
        newsletters = []
    
    # Count statistics
    stats = {
        'total_users': len(users) if isinstance(users, list) else 0,
        'premium_users': sum(1 for user in users if isinstance(users, list) and user.get('subscription_plan') == 'premium'),
        'total_topics': len(topics) if isinstance(topics, list) else 0,
        'total_newsletters': len(newsletters) if isinstance(newsletters, list) else 0
    }
    
    return render_template('admin/dashboard.html', 
                          user_profile=user_profile,
                          users=users,
                          topics=topics,
                          newsletters=newsletters,
                          stats=stats)

@bp.route('/users')
@admin_required
def users():
    # Get all users
    users = supabase.get_all_users()
    
    if isinstance(users, dict) and 'error' in users:
        flash(f'Error fetching users: {users["error"]}', 'danger')
        users = []
    
    return render_template('admin/users.html', users=users)

@bp.route('/set-role/<user_id>', methods=['POST'])
@admin_required
def set_role(user_id):
    role = request.form.get('role')
    
    if not role or role not in ['user', 'admin']:
        flash('Invalid role', 'danger')
        return redirect(url_for('admin.users'))
    
    result = supabase.set_user_role(user_id, role)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error setting role: {result["error"]}', 'danger')
    else:
        flash(f'User role updated to {role} successfully!', 'success')
    
    return redirect(url_for('admin.users'))

@bp.route('/topics')
@admin_required
def topics():
    # Get all topics
    topics = supabase.get_topics(include_predefined=False)
    
    if isinstance(topics, dict) and 'error' in topics:
        flash(f'Error fetching topics: {topics["error"]}', 'danger')
        topics = []
    
    return render_template('admin/topics.html', topics=topics)

@bp.route('/create-topic', methods=['POST'])
@admin_required
def create_topic():
    name = request.form.get('name')
    description = request.form.get('description', '')
    is_predefined = 'is_predefined' in request.form
    
    if not name:
        flash('Topic name is required', 'danger')
        return redirect(url_for('admin.topics'))
    
    result = supabase.create_topic(name, description, is_predefined)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error creating topic: {result["error"]}', 'danger')
    else:
        flash('Topic created successfully!', 'success')
    
    return redirect(url_for('admin.topics'))

@bp.route('/update-topic/<topic_id>', methods=['POST'])
@admin_required
def update_topic(topic_id):
    name = request.form.get('name')
    description = request.form.get('description', '')
    is_predefined = 'is_predefined' in request.form
    
    if not name:
        flash('Topic name is required', 'danger')
        return redirect(url_for('admin.topics'))
    
    data = {
        'name': name,
        'description': description,
        'is_predefined': is_predefined
    }
    
    result = supabase.update_topic(topic_id, data)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error updating topic: {result["error"]}', 'danger')
    else:
        flash('Topic updated successfully!', 'success')
    
    return redirect(url_for('admin.topics'))

@bp.route('/delete-topic/<topic_id>', methods=['POST'])
@admin_required
def delete_topic(topic_id):
    result = supabase.delete_topic(topic_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error deleting topic: {result["error"]}', 'danger')
    else:
        flash('Topic deleted successfully!', 'success')
    
    return redirect(url_for('admin.topics'))

@bp.route('/newsletters')
@admin_required
def newsletters():
    # Get all newsletters
    newsletters = supabase.get_all_newsletters()
    
    # Get all topics for the dropdown
    topics = supabase.get_topics(include_predefined=False)
    
    if isinstance(newsletters, dict) and 'error' in newsletters:
        flash(f'Error fetching newsletters: {newsletters["error"]}', 'danger')
        newsletters = []
    
    if isinstance(topics, dict) and 'error' in topics:
        flash(f'Error fetching topics: {topics["error"]}', 'danger')
        topics = []
    
    return render_template('admin/newsletters.html', newsletters=newsletters, topics=topics)

@bp.route('/create-newsletter', methods=['POST'])
@admin_required
def create_newsletter():
    title = request.form.get('title')
    content = request.form.get('content')
    topic_id = request.form.get('topic_id')
    
    if not title or not content or not topic_id:
        flash('Title, content, and topic are required', 'danger')
        return redirect(url_for('admin.newsletters'))
    
    result = supabase.create_newsletter(title, content, topic_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error creating newsletter: {result["error"]}', 'danger')
    else:
        flash('Newsletter created successfully!', 'success')
    
    return redirect(url_for('admin.newsletters'))

@bp.route('/update-newsletter/<newsletter_id>', methods=['POST'])
@admin_required
def update_newsletter(newsletter_id):
    title = request.form.get('title')
    content = request.form.get('content')
    topic_id = request.form.get('topic_id')
    
    if not title or not content or not topic_id:
        flash('Title, content, and topic are required', 'danger')
        return redirect(url_for('admin.newsletters'))
    
    data = {
        'title': title,
        'content': content,
        'topic_id': topic_id
    }
    
    result = supabase.update_newsletter(newsletter_id, data)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error updating newsletter: {result["error"]}', 'danger')
    else:
        flash('Newsletter updated successfully!', 'success')
    
    return redirect(url_for('admin.newsletters'))

@bp.route('/delete-newsletter/<newsletter_id>', methods=['POST'])
@admin_required
def delete_newsletter(newsletter_id):
    result = supabase.delete_newsletter(newsletter_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error deleting newsletter: {result["error"]}', 'danger')
    else:
        flash('Newsletter deleted successfully!', 'success')
    
    return redirect(url_for('admin.newsletters'))