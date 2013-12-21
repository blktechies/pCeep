from flask import flash, render_template

from app.views import MessageForm
from app.controllers import users, messages


def new_message(user_id):
    return messages.new(user_id)

def get_messages(user_id):
	msgs = messages.get_messages_to(user_id)
	return render_template('messages.html', messages = msgs)


def read_message(user_id, message_id):
	msg = messages.get_message(message_id)
	if msg.receiver_id == user_id:
		messages.mark_message_as('read', msg)
		return render_template('read_message.html', message = msg)


def reply(message_id, user_id):
	msg = messages.get_message(message_id)
	if msg.receiver_id == user_id:
		return render_template('message.html', 
							form = MessageForm( sender_id = user_id,
												receiver = msg.sender.handle,
												title = 're: %s' % (msg.title), 
												body = msg.body))


def send_to(handle, user_id):
	return render_template('message.html', 
							form = MessageForm( sender_id = user_id,
												receiver = handle))

def trash(message_id, user_id):
	msg = messages.get_message(message_id)
	if msg.receiver_id == user_id:
		return messages.destroy(msg)