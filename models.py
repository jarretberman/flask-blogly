"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users."""

    __tablename__: 'users'

    def __repr__(self):
        u=self
        return f'<User id= {u.id} fname = {u.first_name} lname = {u.last_name} img = {u.image_url}>'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),nullable = False)

    last_name = db.Column(db.String(50),nullable = False)

    

    def full_name(self):
        """Concats name strings into one string"""
        return f'{self.first_name} {self.last_name}'

class Post(db.model):
    """Posts."""

    __tablename__ : 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    created_at = db.Column(db)
    post = db.Column(db.String(),nullable = False) 
    title = db.Column(db.String(),nullable = False) 
    user_id = db.Column(db.Integer(),db.ForeignKey(users.id))

    users = db.relationship('User', backref='post')


