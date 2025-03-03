from flask import Blueprint, render_template, redirect, url_for, session
import supabase_client as supabase

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # If user is logged in, redirect to dashboard
    if 'user' in session:
        return redirect(url_for('newsletter.dashboard'))
    return render_template('index.html', supabase=supabase)

@bp.route('/about')
def about():
    return render_template('about.html', supabase=supabase)

@bp.route('/imprint')
def imprint():
    return render_template('imprint.html', supabase=supabase)

@bp.route('/pricing')
def pricing():
    return render_template('pricing.html', supabase=supabase)