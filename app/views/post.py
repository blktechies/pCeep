from flask import flash, render_template

from app.views import CommentForm
from app.controllers import posts


def new_post():
    return posts.new_post()

def get_post(post_title):
    return posts.get_post_by_slug(post_title)

def get_posts():
    return render_template('posts.html', 
                            posts = posts.get_posts())


def get_comments(post_title):
    rslt = posts.get_post_by_slug(post_title)
    return render_template('comments.html', 
                            post = rslt['post'], 
                            comments = rslt['comments'], 
                            comment_count = rslt['comment_count'])


def new_comment(post_title):
    return posts.new_comment(post_title)


def new_reply(post_title, comment_id):
    return posts.new_reply(post_title, comment_id)