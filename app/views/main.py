from flask import flash, render_template

from app.controllers import utils, users, posts
from app.controllers.auth import twitter, github, linkedin
from app.views import ProfileForm


def index(user):
    return render_template('index.html',
                            current_date = utils.get_date(),
                            users = users.get_users())


def oauth_req(network):
    if network == 'twitter':
        return twitter.auth_url()
        
    if network == 'github':
        return github.auth_url()

    if network == 'linkedin':
        return linkedin.auth_url()


def login():
    return render_template('login.html')


def get_profiles():
    return render_template('profiles.html', profiles = users.get_users())


def get_profile_by_id(user_id):
    if(users.get_user(user_id) != None):
        user = users.get_user(user_id)
        social_info = users.get_user_socialinfo(user)
        form = ProfileForm()
        return render_template('profile.html', 
                                user = user,
                                posts = user.posts.all(),
                                user_social_info = social_info,
                                form = form)
    else:
        return render_template('404.html')


def get_profile_by_handle(handle):
    if(users.get_user_by_handle(handle) != None):
        user = users.get_user_by_handle(handle)
        social_info = users.get_user_socialinfo(user)

        form = users.gen_profle_form(user)
        return render_template('profile.html', 
                                user = user,
                                posts = user.posts.all(),
                                user_social_info = social_info,
                                form = form)
    else:
        return render_template('404.html')


def internal_error(error):
    if(error.code == 404):
        return render_template('404.html')

    if(error.code == 500):
        return users.internal_error()