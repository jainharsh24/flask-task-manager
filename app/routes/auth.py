
from flask import Blueprint , render_template , redirect , url_for , flash , session ,request
from app.models import User
from app import db
auth_bp = Blueprint('auth' , __name__)


@auth_bp.route('/login', methods=['GET' , 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('tasks.view_tasks'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session['user'] = username
            flash('Login Successfull' , 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET' , 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        new_user = User(username = username , password = password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('/register.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user' , None)
    flash('Logged out' , 'info')
    return redirect(url_for('auth.login'))

