from flask import flash, g, redirect, render_template, request, url_for, session
from sqlalchemy import exc, desc

from app import app, db
from app.models import Post, Comment, Comment_Reply
from app.views import PostForm, CommentForm
from app.controllers import utils



def get_post(id):
		id = unicode(int(id))
		return Post.query.get(id)


def get_posts():
		rslts = []
		posts = Post.query.order_by(desc(Post.last_updated)).all()
		for post in posts:
			# this cant be fast... refactor
			post.comment_count = count_comments(post.id)
			rslts.append(post)
		return rslts


def get_post_by_slug(post_title):
	post = Post.query.filter_by(slug = post_title).first()
	count = 0
	for c in post.comments:
		count += 1
		for r in c.replies.all():
			count +=1
	comments = post.comments.order_by(desc('last_updated')).all()
	return dict(post = post, comments = comments, comment_count = count)


def new_post():
		form = PostForm(user_id = g.user.id)
		return render_template('post.html', form = form)


def create_post(params):
		post = Post(params['user_id'], params['title'], params['body'])
		db.session.add(post)
		db.session.commit()
		flash("Success: Your post, '%s', has been created" % (post.title))
		return redirect(url_for('get_profile_by_handle', handle = g.user.handle))


def get_comment(comment_id):
		id = unicode(int(comment_id))
		return Comment.query.get(id)


def get_comments(post_id):
		post_id = unicode(int(post_id))
		post = get_post(post_id)
		return dict(title = post.title, 
					comments = post.comments.order_by(desc(last_updated)).all())


def new_comment(post_title):
	rslt = get_post_by_slug(post_title)
	return render_template('comment.html', 
							form = CommentForm(user_id	= g.user.id,
												post_id = rslt['post'].id),
							post = rslt['post'])


def new_reply(post_title, comment_id):
	comment = get_comment(comment_id)
	return render_template('comment.html', 
							form     = CommentForm(user_id  	= g.user.id,
													post_id     = comment.post.id, 
													comment_id  = comment.id),
							title    = comment.post.title,
							comment  = comment)


def create_comment(params, post_title):
		comment = Comment(params['user_id'], params['post_id'], params['body'])
		db.session.add(comment)
		db.session.commit()
		flash("Your comment has been receieved")
		return redirect(url_for('get_comments', post_title = post_title))


def create_reply(params, post_title):
		reply = Comment_Reply(params['user_id'], params['comment_id'], params['body'])
		db.session.add(reply)
		db.session.commit()
		flash("Your response has been receieved")
		return redirect(url_for('get_comments', post_title = post_title))


def count_comments(post_id):
	post = get_post(post_id)
	count = 0
	for c in post.comments:
		count += 1
		for r in c.replies.all():
			count +=1
	return count
