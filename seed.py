
from models import db, User
from app import app

db.drop_all()
db.create_all()
User.query.delete()

db.session.add(User(first_name='bob', last_name='bob'))
db.session.add(User(first_name='john', last_name='bob'))
db.session.add(User(first_name='james', last_name='bob'))
db.session.add(User(first_name='Big', last_name='bob'))
db.session.add(User(first_name='dog', last_name='bob'))

db.session.commit()