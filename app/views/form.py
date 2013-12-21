from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField, HiddenField
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app import db
from app.models import Description, Interest


def all_descriptions():
    return Description.query.all()
    
class WelcomeForm(Form):
    network         = HiddenField('network')
    name            = HiddenField('name')
    username        = HiddenField('username')
    profile_image   = HiddenField('profile_image')
    network_url     = HiddenField('network_url')
    network_id      = HiddenField('network_id')
    email           = TextField('email', validators = [Required()])


class ProfileForm(Form):
    user_id         = HiddenField('user_id')
    handle          = TextField('handle', validators = [Required()])
    display_name    = TextField('display_name', validators = [Required()])
    email           = TextField('email', validators = [Required()])
    description     = QuerySelectField('description', query_factory = all_descriptions)
    status          = TextAreaField('status')


class PostForm(Form):
    user_id         = HiddenField('user_id')
    title           = TextField('title', validators = [Required()])
    body            = TextAreaField('body', validators = [Required()])


class CommentForm(Form):
    user_id         = HiddenField('user_id')
    post_id         = HiddenField('post_id')
    comment_id      = HiddenField('comment_id')
    body            = TextAreaField('body', validators = [Required()])


class MessageForm(Form):
    sender_id       = HiddenField('sender_id')
    receiver        = TextField('receiver', validators = [Required()])
    title           = TextField('title', validators = [Required()])
    body            = TextAreaField('body', validators = [Required()])