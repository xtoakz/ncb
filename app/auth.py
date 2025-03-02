from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
import supabase_client as supabase

bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'danger')
            return render_template('auth/signup.html')
        
        response = supabase.sign_up(email, password)
        
        if 'error' in response:
            flash(f'Error: {response["error"]}', 'danger')
            return render_template('auth/signup.html')
        
        flash('Registration successful! Please check your email to confirm your account.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

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
            'id': response['user']['id'],
            'email': response['user']['email'],
            'access_token': response['session']['access_token']
        }
        
        flash('Login successful!', 'success')
        return redirect(url_for('todo.dashboard'))
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    if 'user' in session:
        access_token = session['user'].get('access_token')
        if access_token:
            supabase.sign_out(access_token)
        session.pop('user', None)
    
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@bp.route('/profile')
@login_required
def profile():
    user = session.get('user', {})
    return render_template('auth/profile.html', user=user)