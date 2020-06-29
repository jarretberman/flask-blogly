
from models import db, User, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()
User.query.delete()

db.session.add(User(first_name='bob', last_name='bob'))
db.session.add(User(first_name='john', last_name='bob'))
db.session.add(User(first_name='james', last_name='bob'))
db.session.add(User(first_name='Big', last_name='bob'))
db.session.add(User(first_name='dog', last_name='bob'))

db.session.add(Post(title = 'my post', post = 'my post text', user_id = 1))
db.session.add(Post(title = 'my post', post = 'my post text', user_id = 1))
db.session.add(Post(title = 'my post', post = 'my post text', user_id = 2))
db.session.add(Post(title = 'my post', post = 'my post text', user_id = 3))
db.session.add(Post(title = 'my post', post = 'my post text', user_id = 3))
db.session.add(Post(title = 'my post', post = 'my post text', user_id = 3))

db.session.add(Tag(name='fun'))
db.session.add(Tag(name='cool'))
db.session.add(Tag(name='tech'))

db.session.add(PostTag(post_id=1,tag_id=1))
db.session.add(PostTag(post_id=2,tag_id=1))
db.session.add(PostTag(post_id=1,tag_id=2))
db.session.add(PostTag(post_id=1,tag_id=3))
db.session.add(PostTag(post_id=3,tag_id=1))
db.session.add(PostTag(post_id=3,tag_id=2))


db.session.commit()