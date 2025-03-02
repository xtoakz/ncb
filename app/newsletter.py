from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.auth import login_required
import supabase_client as supabase

bp = Blueprint('newsletter', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user', {}).get('id')
    newsletters = supabase.get_newsletters(user_id)
    
    if isinstance(newsletters, dict) and 'error' in newsletters:
        flash(f'Error fetching newsletters: {newsletters["error"]}', 'danger')
        newsletters = []
    
    return render_template('newsletter/dashboard.html', newsletters=newsletters)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    user_id = session.get('user', {}).get('id')
    title = request.form.get('title')
    content = request.form.get('content', '')
    delivery_platform = request.form.get('delivery_platform', 'whatsapp')
    
    if not title:
        flash('Title is required', 'danger')
        return redirect(url_for('newsletter.dashboard'))
    
    result = supabase.create_newsletter(user_id, title, content, delivery_platform)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error creating newsletter: {result["error"]}', 'danger')
    else:
        flash('Newsletter created successfully!', 'success')
    
    return redirect(url_for('newsletter.dashboard'))

@bp.route('/update/<newsletter_id>', methods=['POST'])
@login_required
def update(newsletter_id):
    title = request.form.get('title')
    content = request.form.get('content', '')
    delivery_platform = request.form.get('delivery_platform', 'whatsapp')
    status = request.form.get('status', 'draft')
    
    if not title:
        flash('Title is required', 'danger')
        return redirect(url_for('newsletter.dashboard'))
    
    data = {
        'title': title,
        'content': content,
        'delivery_platform': delivery_platform,
        'status': status
    }
    
    result = supabase.update_newsletter(newsletter_id, data)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error updating newsletter: {result["error"]}', 'danger')
    else:
        flash('Newsletter updated successfully!', 'success')
    
    return redirect(url_for('newsletter.dashboard'))

@bp.route('/delete/<newsletter_id>', methods=['POST'])
@login_required
def delete(newsletter_id):
    result = supabase.delete_newsletter(newsletter_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error deleting newsletter: {result["error"]}', 'danger')
    else:
        flash('Newsletter deleted successfully!', 'success')
    
    return redirect(url_for('newsletter.dashboard'))

@bp.route('/send/<newsletter_id>', methods=['POST'])
@login_required
def send(newsletter_id):
    result = supabase.send_newsletter(newsletter_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error sending newsletter: {result["error"]}', 'danger')
    else:
        flash('Newsletter sent successfully!', 'success')
    
    return redirect(url_for('newsletter.dashboard'))

@bp.route('/get_news', methods=['POST'])
def get_news():
    topic = request.json.get('topic', '')
    
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400
    
    result = supabase.get_news(topic)
    
    if isinstance(result, dict) and 'error' in result:
        return jsonify({'error': result['error']}), 400
    
    return jsonify(result)