
import secrets

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy #use to talk to database
from sqlalchemy import inspect, text

#create database oblect globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__) #object created

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_INSTANCE_TOKEN'] = secrets.token_hex(16)

    db.init_app(app)  

    @app.before_request
    def clear_stale_session_after_restart():
        stored_token = session.get('session_instance_token')
        current_token = app.config['SESSION_INSTANCE_TOKEN']

        if stored_token and stored_token != current_token:
            session.clear()

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app

def ensure_schema_updates(app):
    with app.app_context():
        inspector = inspect(db.engine)
        if 'task' not in inspector.get_table_names():
            return

        columns = {column['name'] for column in inspector.get_columns('task')}
        if 'user_id' not in columns:
            with db.engine.begin() as connection:
                connection.execute(text("ALTER TABLE task ADD COLUMN user_id INTEGER"))
