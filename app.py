"""Blogly application."""

from flask import Flask, redirect, session,  render_template, request, flash
from models import db, connect_db, User, Post, Tag
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
    posts = Post.query.filter_by(user_id = user.id).all()
    

    return render_template('profile.html', user=user, posts = posts)

@app.route('/users/<int:id>/edit')
def userEdit(id):
    """Edit a user profile"""
    user = User.query.get(id)
    return render_template('editprofile.html', user=user)

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

@app.route('/users/<int:userid>/posts/new')
def newpostForm(userid):
    """Form to make a new Post"""
    tags = Tag.query.all()
    return render_template('/newpost.html', userid = userid,tags=tags)

@app.route('/users/<int:userid>/posts/new', methods= ['POST'])
def handle_new_post(userid):
    """adds new post to the database"""
    new_post = Post(title=request.form['title'],post=request.form['post'],user_id = userid)
    title, post, *tags = request.form

    taglist = db.session.query(Tag).filter(Tag.name.in_( tuple(tags))).all()

    for tag in taglist:
        new_post.tags.append(tag)


    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{userid}')

@app.route('/posts/<int:postid>/edit')
def edit_post(postid):
    """renders edit post template"""
    post = Post.query.get_or_404(postid)
    tot_tags= Tag.query.all()

    return render_template('editpost.html', post = post,tot_tags=tot_tags)

@app.route('/posts/<int:postid>/edit', methods=['POST'])
def handle_post_edit(postid):
    """update post in database"""

    post = Post.query.get_or_404(postid)
    post.title = request.form['title']
    post.post = request.form['post']
    title, _post, *tags = request.form

    taglist = db.session.query(Tag).filter(Tag.name.in_(tuple(tags))).all()
    for tag in taglist:
        post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{postid}')


@app.route('/posts/<int:postid>')
def postPage(postid):
    """Page for a specific Post"""

    post = Post.query.get_or_404(postid)

    return render_template('post.html', post=post)

@app.route('/posts/<int:postid>/delete', methods=['POST'])
def delete_post(postid):
    """Delete a Post"""
    userid = db.session.query(Post.user_id).filter_by(id=postid).one()

    Post.query.filter_by(id=postid).delete()
    db.session.commit()
    return redirect(f'/users/{userid[0]}')

@app.route('/tags')
def tags_page():
    """Shows all tags and gives option to create them"""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tagid>')
def tag_pag(tagid):
    """Page for individual tags"""
    tag = Tag.query.get(tagid)
    return render_template('tagprofile.html', tag = tag)

@app.route('/tags/new')
def new_tag():
    """Users can create a new tag"""

    return render_template('newtag.html')

@app.route('/tags/new', methods=['POST'])
def handle_new_tag():

    tag = Tag(name=request.form['name'],description= request.form['desc'] if request.form['desc'] else None )

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/edit/<int:tagid>')
def tag_edit_form(tagid):
    """Lets Users Edit Tags"""

    tag = Tag.query.get(tagid)

    return render_template('edittag.html', tag =tag)

@app.route('/tags/edit/<int:tagid>', methods=['POST'])
def handle_tag_edit(tagid):
    """Updates tag in database"""

    tag = Tag.query.get(tagid)
    tag.name = request.form['name']
    tag.description = request.form['desc'] if request.form['desc'] else None

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/delete/<int:tagid>')
def delete_tag(tagid):
    Tag.query.filter_by(id=tagid).delete()

    return redirect('/tags')

    