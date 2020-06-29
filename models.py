"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    image_url = db.Column(db.String(), nullable = False, default = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRDn0QJj1_iTjhjVAZG1jllcq2kv1BeiUCKsw&usqp=CAU')

    

    def full_name(self):
        """Concats name strings into one string"""
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Posts."""

    __tablename__ : 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    created_at = db.Column(db.DateTime(), default = datetime.today())
    post = db.Column(db.String(),nullable = False) 
    title = db.Column(db.String(),nullable = False) 
    user_id = db.Column(db.Integer(),db.ForeignKey(User.id, ondelete='cascade'))

    PTrel = db.relationship('PostTag', backref = 'post')
    tags = db.relationship('Tag', secondary='post_tag', backref='posts')
    users = db.relationship('User', backref ='post')




    


class Tag(db.Model):
    __tablename__ : 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text(), unique = True, nullable=False)
    description = db.Column(db.Text())

    PTrel = db.relationship('PostTag', backref = 'tag')


class PostTag(db.Model):

    __tablename__: 'posts_tags'

    post_id = db.Column(db.Integer(), db.ForeignKey(Post.id, ondelete='cascade' ), primary_key=True)
    tag_id = db.Column(db.Integer(), db.ForeignKey(Tag.id, ondelete='cascade'), primary_key=True )