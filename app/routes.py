from flask import Blueprint, render_template, redirect, url_for, session

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # If user is logged in, redirect to newsletter dashboard
    if 'user' in session:
        return redirect(url_for('newsletter.dashboard'))
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/imprint')
def imprint():
    return render_template('imprint.html')