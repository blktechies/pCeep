from flask import g, redirect, request, session
from flask.ext.login import current_user, login_required

from app import app, db, lm
from app.models import User, Post
from app.views import CommentForm, PostForm, ProfileForm, MessageForm, WelcomeForm, main, post, message
from app.controllers import users, posts, messages, utils

from datetime import datetime

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        g.user.unread_messages = messages.count_unread(g.user.id)
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    return main.index(g.user)


@app.route('/login/<social_network>')
def get_login(social_network):
    oauth_req = main.oauth_req(social_network)
    try:
        session['state'] = oauth_req['state']
    except:
        pass
    return redirect(oauth_req['url'])

@app.route('/login')
def login():
    return main.login()


@app.route('/auth/<social_network>', methods = ['GET', 'POST'])
def get_auth_req(social_network):
    form = WelcomeForm()
    if form.validate_on_submit():
        return users.complete_user_setup(request.values)
    return users.get_or_create_login(social_network)


@app.route('/users/<int:id>')
def get_profile_by_id(id):
    return main.get_profile_by_id(id)


@app.route('/profiles')
def get_profiles():
    return main.get_profiles()


@app.route('/profiles/<handle>', methods = ['GET', 'POST'])
def get_profile_by_handle(handle):
    form = ProfileForm()
    if form.validate_on_submit():
        return users.update_profile(request.values)
    return main.get_profile_by_handle(handle)


@app.route('/posts')
def all_posts():
    return post.get_posts()

@app.route('/post', methods = ['GET', 'POST'])
@login_required
def create_post():
    form = PostForm(user_id = g.user.id)
    if form.validate_on_submit():
        return posts.create_post(request.values)
    return post.new_post()


@app.route('/<post_title>/comments')
def get_comments(post_title):
    return post.get_comments(post_title)


@app.route('/<post_title>/comment', methods = ['GET', 'POST'])
@login_required
def leave_comment(post_title):
    form = CommentForm()
    if form.validate_on_submit():
        return posts.create_comment(request.values, post_title)
    return post.new_comment(post_title)

@app.route('/<post_title>/reply/to/comment/<comment_id>', methods = ['GET', 'POST'])
@login_required
def reply_to_comment(post_title, comment_id):
    form = CommentForm()
    if form.validate_on_submit():
        return posts.create_reply(request.values, post_title)
    return post.new_reply(post_title, comment_id)

@app.route('/messages')
@login_required
def get_messages():
    return message.get_messages(g.user.id)

@app.route('/message', methods = ['GET', 'POST'])
@login_required
def new_message():
    form = MessageForm()
    if form.validate_on_submit():
        return messages.create_message(request.values)
    return message.new_message(g.user.id)


@app.route('/read/message/<message_id>')
@login_required
def read_message(message_id):
    return message.read_message(g.user.id, message_id)


@app.route('/reply/to/message/<message_id>')
@login_required
def message_reply(message_id):
    return message.reply(message_id, g.user.id)

@app.route('/send/message/to/<handle>')
@login_required
def send_message_to(handle):
    return message.send_to(handle, g.user.id)


@app.route('/trash/message/<message_id>')
@login_required
def message_trash(message_id):
    return message.trash(message_id, g.user.id)


@app.route('/logout')
@login_required
def logout():
    return users.logout()


@app.errorhandler(404)
def internal_error(error):
    return main.internal_error(error)


@app.errorhandler(500)
def internal_error(error):
    return main.internal_error(error)