from app import db
from app.controllers import utils

class Description(db.Model):
    id      = db.Column(db.Integer, primary_key = True)
    title   =  db.Column(db.String(30))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<description: %r>' % (self.title)

    def __str__(self):
        return self.title


class User(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    description_id  = db.Column(db.Integer, db.ForeignKey('description.id'))
    email           = db.Column(db.String(120), unique = True)
    display_name    = db.Column(db.String(255))
    handle          = db.Column(db.String(30), unique = True)
    image_url       = db.Column(db.String(512))
    social_handles  = db.relationship('SocialUser',
                                        backref = 'user',
                                        lazy = 'dynamic')
    posts           = db.relationship('Post',
                                        backref = 'user',
                                        lazy = 'dynamic')
    comments        = db.relationship('Comment',
                                        backref = 'user',
                                        lazy = 'dynamic')
    replies         = db.relationship('Comment_Reply',
                                        backref = 'user',
                                        lazy = 'dynamic')
    messages        = db.relationship('Message',
                                        backref = 'sender',
                                        lazy = 'dynamic')
    interests       = db.relationship('Interest',
                                        backref = 'user',
                                        lazy = 'dynamic')
    status          = db.Column(db.String(140))
    date_created    = db.Column(db.DateTime)
    last_updated    = db.Column(db.DateTime)
    last_seen       = db.Column(db.DateTime)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def get_unique_handle(handle):
        if User.query.filter_by(handle = handle).first() == None:
            return handle
        version = 2
        while True:
            new_handle = handle + str(version)
            if User.query.filter_by(handle = new_handle).first() == None:
                break
            version += 1
        return new_handle

    def __init__(self, email, display_name, image_url):
        self.email          = email
        self.display_name   = display_name
        self.handle         = self.get_unique_handle("".join(display_name.split()).lower())
        self.image_url      = image_url
        self.status         = 'Just joined.'
        self.description_id = 1
        self.date_created   = utils.get_timestamp()
        self.last_updated   = utils.get_timestamp()

    def __repr__(self):
        return '<User %r>' % (self.display_name)


class SocialUser(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    network         = db.Column(db.String(15))
    network_id      = db.Column(db.String(30))
    username        = db.Column(db.String(30))
    network_url     = db.Column(db.String(255))
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, network, network_id, username, network_url):
        self.network        = network
        self.network_id     = network_id
        self.username       = username
        self.network_url    = network_url

    def __repr__(self):
        return '<%r, %r>' % (self.network, self.username)


class Message(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id     = db.Column(db.Integer)
    title           = db.Column(db.String(50))
    body            = db.Column(db.String(512))
    viewed          = db.Column(db.Boolean, default = False)
    date_created    = db.Column(db.DateTime)

    def __init__(self, user_id, receiver_id, title, body):
        self.user_id        = user_id
        self.receiver_id    = receiver_id
        self.title          = title
        self.body           = body
        self.date_created   = utils.get_timestamp()

    def __repr__(self):
        return '<msg to %r from %r on %r>' % (User.query.get(self.receiver_id), 
                                                User.query.get(self.user_id), 
                                                self.date_created)

class Interest(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    speciality  = db.Column(db.String(50))


    def __init__(self, user_id, speciality):
        self.user_id        = user_id
        self.speciality     = speciality

    def __repr__(self):
        return '<%r interested in %r>' % (User.query.get(self.user_id), 
                                                self.speciality)
