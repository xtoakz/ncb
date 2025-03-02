from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.auth import login_required
import supabase_client as supabase

bp = Blueprint('todo', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user', {}).get('id')
    todos = supabase.get_todos(user_id)
    
    if isinstance(todos, dict) and 'error' in todos:
        flash(f'Error fetching todos: {todos["error"]}', 'danger')
        todos = []
    
    return render_template('todo/dashboard.html', todos=todos)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    user_id = session.get('user', {}).get('id')
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    if not title:
        flash('Title is required', 'danger')
        return redirect(url_for('todo.dashboard'))
    
    result = supabase.create_todo(user_id, title, description)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error creating todo: {result["error"]}', 'danger')
    else:
        flash('Todo created successfully!', 'success')
    
    return redirect(url_for('todo.dashboard'))

@bp.route('/update/<todo_id>', methods=['POST'])
@login_required
def update(todo_id):
    title = request.form.get('title')
    description = request.form.get('description', '')
    completed = 'completed' in request.form
    
    if not title:
        flash('Title is required', 'danger')
        return redirect(url_for('todo.dashboard'))
    
    data = {
        'title': title,
        'description': description,
        'completed': completed
    }
    
    result = supabase.update_todo(todo_id, data)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error updating todo: {result["error"]}', 'danger')
    else:
        flash('Todo updated successfully!', 'success')
    
    return redirect(url_for('todo.dashboard'))

@bp.route('/delete/<todo_id>', methods=['POST'])
@login_required
def delete(todo_id):
    result = supabase.delete_todo(todo_id)
    
    if isinstance(result, dict) and 'error' in result:
        flash(f'Error deleting todo: {result["error"]}', 'danger')
    else:
        flash('Todo deleted successfully!', 'success')
    
    return redirect(url_for('todo.dashboard'))

@bp.route('/toggle/<todo_id>', methods=['POST'])
@login_required
def toggle(todo_id):
    completed = request.json.get('completed', False)
    
    result = supabase.update_todo(todo_id, {'completed': completed})
    
    if isinstance(result, dict) and 'error' in result:
        return jsonify({'success': False, 'error': result['error']}), 400
    
    return jsonify({'success': True})