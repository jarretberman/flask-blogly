"""Blogly application."""

from flask import Flask, redirect, session,  render_template, request, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route('/')
def homeRedirect():
    """Function that redirects to users page"""

    return redirect('/users')

@app.route('/users')
def usersPage():
    """Function that lists all users in the db"""

    users = User.query.all()

    return render_template('users.html', users=users)

@app.route('/users/new')
def createUser():
    """Form to add a new user to database"""

    return render_template('newUser.html')

@app.route('/users/new', methods=["POST"])
def newUserPost():
    """Handles form submission for new users"""

    first = request.form['first']
    last = request.form['last']
    img = request.form['img'] if request.form['img'] else None

    user = User(first_name=first,last_name=last,image_url=img)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>')
def userProfile(id):
    """Displays User Profile"""

    user = User.query.get_or_404(id)

    return render_template('profile.html', user=user)

@app.route('/users/<int:id>/edit')
def userEdit(id):
    """Edit a user profile"""
    user = User.query.get(id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:id>/edit',  methods=["POST"])
def updateUser(id):
    """Processes Edit form"""

    user = User.query.get(id)
   
    user.first_name =request.form['first']
    user.last_name =request.form['last']
    user.image_url =request.form['img']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>/delete',  methods=["POST"])
def deleteUser(id):
    """Deletes a User"""

    User.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect('/users')