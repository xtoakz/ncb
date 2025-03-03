from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
import supabase_client as supabase
import re

bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login', next=request.url))
        
        user_id = session['user'].get('id')
        user_profile = supabase.get_user_profile(user_id)
        
        if not user_profile or user_profile.get('role') != 'admin':
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.index'))
            
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        
        # Validate inputs
        if not email or not password:
            flash('Email and password are required', 'danger')
            return render_template('auth/signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('auth/signup.html')
        
        if phone_number and not re.match(r'^\+?[0-9]{10,15}$', phone_number):
            flash('Please enter a valid phone number', 'danger')
            return render_template('auth/signup.html')
        
        # Register user
        response = supabase.sign_up(email, password, full_name, phone_number)
        
        if 'error' in response:
            flash(f'Error: {response["error"]}', 'danger')
            return render_template('auth/signup.html')
        
        # Create user profile
        supabase.create_user_profile(response['user']['id'], full_name, phone_number)
        
        flash('Registration successful! Please check your email to confirm your account.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html', supabase=supabase)

@bp.route('/signup/google')
def signup_google():
    response = supabase.sign_up_with_google()
    
    if 'error' in response:
        flash(f'Error: {response["error"]}', 'danger')
        return redirect(url_for('auth.signup'))
    
    # Redirect to Google OAuth URL
    return redirect(response['url'])

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'danger')
            return render_template('auth/login.html')
        
        response = supabase.sign_in(email, password)
        
        if 'error' in response:
            flash(f'Error: {response["error"]}', 'danger')
            return render_template('auth/login.html')
        
        # Store user data in session
        session['user'] = {
            'id': response.user.id,
            'email': response.user.email,
            'access_token': response.session.access_token
        }
        
        # Get user profile
        user_profile = supabase.get_user_profile(response.user.id)
        
        # Check if user is admin
        if user_profile and user_profile.get('role') == 'admin':
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin.dashboard'))

        # Update user data in session
        session['user'] = {
            'id': response.user.id,
            'email': response.user.email,
            'access_token': response.session.access_token
        }

        flash('Login successful!', 'success')
        return redirect(url_for('newsletter.dashboard'))
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    if 'user' in session:
        access_token = session['user'].get('access_token')
        print(f"Access token: {access_token}")
        if access_token:
            supabase.sign_out(access_token)
        session.pop('user', None)
    
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session.get('user', {}).get('id')
    user_email = session.get('user', {}).get('email')
    
    # Get user profile
    user_profile = supabase.get_user_profile(user_id)
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        
        # Validate phone number
        if phone_number and not re.match(r'^\+?[0-9]{10,15}$', phone_number):
            flash('Please enter a valid phone number', 'danger')
            return render_template('auth/profile.html', user=session.get('user', {}), profile=user_profile)
        
        # Update profile
        data = {
            'full_name': full_name,
            'phone_number': phone_number
        }
        
        result = supabase.update_user_profile(user_id, data)
        
        if isinstance(result, dict) and 'error' in result:
            flash(f'Error updating profile: {result["error"]}', 'danger')
        else:
            flash('Profile updated successfully!', 'success')
            # Update user_profile with new data
            user_profile = supabase.get_user_profile(user_id)
    
    # Get user's subscribed topics
    user_topics = supabase.get_user_topics(user_id)
    
    # Get all available topics
    all_topics = supabase.get_topics()
    
    # Prepare data for template
    user_data = {
        'id': user_id,
        'email': user_email,
        'profile': user_profile,
        'topics': user_topics if isinstance(user_topics, list) else [],
        'all_topics': all_topics if isinstance(all_topics, list) else []
    }
    
    print(f"User profile: {user_profile}")
    return render_template('auth/profile.html', user=user_data, supabase=supabase)

@bp.route('/verify-phone', methods=['POST'])
@login_required
def verify_phone():
    user_id = session.get('user', {}).get('id')
    phone_number = request.form.get('phone_number')
    verification_code = request.form.get('verification_code')
    
    # In a real application, you would send an SMS with a verification code
    # and verify it here. For this example, we'll just mark the phone as verified.
    
    # Validate phone number
    if not phone_number or not re.match(r'^\+?[0-9]{10,15}$', phone_number):
        flash('Please enter a valid phone number', 'danger')
        return redirect(url_for('auth.profile'))
    
    # For demo purposes, accept any 6-digit code
    if not verification_code or not re.match(r'^[0-9]{6}$', verification_code):
        flash('Please enter a valid 6-digit verification code', 'danger')
        return redirect(url_for('auth.profile'))
    
    # Mark phone as verified
    result = supabase.verify_phone(user_id, phone_number)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error verifying phone: {result["error"]}', 'danger')
    else:
        flash('Phone number verified successfully!', 'success')
    
    return redirect(url_for('auth.profile'))

@bp.route('/subscribe-topic/<topic_id>', methods=['POST'])
@login_required
def subscribe_topic(topic_id):
    user_id = session.get('user', {}).get('id')
    
    result = supabase.subscribe_to_topic(user_id, topic_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error subscribing to topic: {result["error"]}', 'danger')
    else:
        flash('Subscribed to topic successfully!', 'success')
    
    return redirect(url_for('auth.profile'))

@bp.route('/promote_to_admin/<user_id>', methods=['POST'])
@login_required
def promote_to_admin(user_id):
    # Get user profile
    user_profile = supabase.get_user_profile(user_id)
    
    if not user_profile:
        flash('User not found', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    # Update user role to admin
    result = supabase.update_user_profile(user_id, {'role': 'admin'})
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error promoting user to admin: {result["error"]}', 'danger')
    else:
        flash('User promoted to admin successfully!', 'success')
    
    return redirect(url_for('admin.dashboard'))

@bp.route('/unsubscribe-topic/<topic_id>', methods=['POST'])
@login_required
def unsubscribe_topic(topic_id):
    user_id = session.get('user', {}).get('id')
    
    result = supabase.unsubscribe_from_topic(user_id, topic_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error unsubscribing from topic: {result["error"]}', 'danger')
    else:
        flash('Unsubscribed from topic successfully!', 'success')
    
    return redirect(url_for('auth.profile'))

@bp.route('/upgrade', methods=['GET', 'POST'])
@login_required
def upgrade():
    user_id = session.get('user', {}).get('id')
    user_profile = supabase.get_user_profile(user_id)
    
    if request.method == 'POST':
        # In a real application, you would process payment here
        # For this example, we'll just update the subscription plan
        
        result = supabase.update_subscription_plan(user_id, 'premium')
        
        if isinstance(result, dict) and 'error' in result:
            flash(f'Error upgrading subscription: {result["error"]}', 'danger')
        else:
            flash('Upgraded to Premium successfully!', 'success')
            return redirect(url_for('auth.profile'))
    
    return render_template('auth/upgrade.html', user_profile=user_profile, supabase=supabase)