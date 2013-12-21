from app import db
from app.controllers import utils

class Post(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    title           = db.Column(db.String(50))
    body            = db.Column(db.String(512))
    slug            = db.Column(db.String(256), unique = True)
    comments        = db.relationship('Comment',
                                        backref = 'post',
                                        lazy = 'dynamic')
    date_created    = db.Column(db.DateTime)
    last_updated    = db.Column(db.DateTime)


    @staticmethod
    def get_unique_slug(title):
        slug = utils.slug(title)
        if Post.query.filter_by(slug = slug).first() == None:
            return slug
        version = 2
        while True:
            new_slug = slug + '-' + str(version)
            if Post.query.filter_by(slug = new_slug).first() == None:
                break
            version += 1
        return new_slug

    def __init__(self, user_id, title, body):
        self.user_id        = user_id
        self.title          = title
        self.body           = body
        self.slug           = self.get_unique_slug(title)
        self.date_created   = utils.get_timestamp()
        self.last_updated   = utils.get_timestamp()

    def __repr__(self):
        return '<%r>' % (self.title)


class Comment(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id         = db.Column(db.Integer, db.ForeignKey('post.id'))
    body            = db.Column(db.String(512))
    replies         = db.relationship('Comment_Reply',
                                        backref = 'parent',
                                        lazy = 'dynamic')
    date_created    = db.Column(db.DateTime)
    last_updated    = db.Column(db.DateTime)

    def __init__(self, user_id, post_id, body):
        self.user_id        = user_id
        self.post_id        = post_id
        self.body           = body
        self.date_created   = utils.get_timestamp()
        self.last_updated   = utils.get_timestamp()

    def __repr__(self):
        return '<comment from %r>' % (self.user.display_name)


class Comment_Reply(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id      = db.Column(db.Integer, db.ForeignKey('comment.id'))
    body            = db.Column(db.String(512))
    date_created    = db.Column(db.DateTime)
    last_updated    = db.Column(db.DateTime)

    def __init__(self, user_id, comment_id, body):
        self.user_id        = user_id
        self.comment_id     = comment_id 
        self.body           = body
        self.date_created   = utils.get_timestamp()
        self.last_updated   = utils.get_timestamp()

    def __repr__(self):
        return '<reply from %r>' % (self.user.display_name)