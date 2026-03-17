
from flask import Blueprint , render_template , request , flash , session , redirect , url_for 
from app import db
from app.models import Task, User

tasks_bp = Blueprint('tasks' , __name__)

def get_logged_in_user():
    username = session.get('user')
    if not username:
        return None
    return User.query.filter_by(username=username).first()

@tasks_bp.route('/')
def view_tasks():
    user = get_logged_in_user()
    tasks = []
    if user:
        tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('tasks.html' , tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='Pending', user_id=user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully' , 'success')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('auth.login'))
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('auth.login'))
    Task.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    flash('All tasks cleared!' , 'info')
    return redirect(url_for('tasks.view_tasks'))



