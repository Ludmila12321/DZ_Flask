from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(80), nullable=False)
    terms = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return f'User({self.surname} {self.name} {self.email})'