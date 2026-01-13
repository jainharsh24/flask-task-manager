
from app import db

class Task(db.Model):
    id = db.Column(db.Integer , primary_key= True)
    title = db.Column(db.String(100), nullable =False)
    status = db.Column(db.String(20), default = "pending")

class User(db.Model):
        id = db.Column(db.Integer , primary_key= True)
        username = db.Column(db.String(200), unique=True)
        password = db.Column(db.String(200), nullable=False)

        def __init__(self,username,password):
            self.username = username
            self.password=password

