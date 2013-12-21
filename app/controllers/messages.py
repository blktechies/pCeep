from flask import flash, g, redirect, render_template, request, url_for, session
from sqlalchemy import exc, desc

from app import app, db
from app.models import Message
from app.views import MessageForm
from app.controllers import users, utils


def new(user_id):
	return render_template('message.html', 
							form = MessageForm(sender_id = user_id))


def create_message(params):
	'''
		This is gonna require some validation 
	'''
	receiver = users.get_user_by_handle(params['receiver'])
	if not receiver == None:
		msg = Message(params['sender_id'], receiver.id, params['title'], params['body'])
		db.session.add(msg)
		db.session.commit()
		flash('Success: Your message to %s has been sent' %(params['receiver']))
		return redirect(url_for('new_message'))

	else:
		flash("Warning: User, '%s', is not found in the system" % (params['receiver']))
		return render_template('message.html', 
								form = MessageForm( title = params['title'], 
													body = params['body']))


def get_messages_to(user_id):
	id = unicode(int(user_id))
	return Message.query.filter_by(receiver_id = id).all()


def get_message(message_id):
	id = unicode(int(message_id))
	return Message.query.get(id)	


def count_unread(user_id):
	return Message.query.filter_by(receiver_id = user_id, viewed = False).count()


def mark_message_as(mark, msg):
	if mark == 'read':
		msg.viewed = True
		
	elif mark == 'undread':
		msg.viewed = False

	db.session.add(msg)
	db.session.commit()


def destroy(message):
	try:
		db.session.delete(message)
		db.session.commit()
		flash('Success: This message has been deleted')
	except:
		db.session.rollback()
		flash('Warning: An error has occured')
	
	return redirect(url_for('get_messages'))

