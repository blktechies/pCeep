#!/usr/bin/env python
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
import datetime
import os.path

from app import db
from app.models import  User, Message
from app.controllers import utils

import random

import seed_data

titles = seed_data.COMMENTS

today = datetime.datetime.utcnow()
last_month = datetime.date(day=1, month=today.month, year=today.year) - datetime.timedelta(days=30)
users = User.query.all()
del users[-1]
receiver = User.query.all()[-1]

def seed_data():
    try:
        for x in range(0, 10):
            date_created = utils.random_date(receiver.date_created, 
                                                datetime.datetime.utcnow())
            sender = random.sample(users, 1)[0]
            subject = random.sample(['RE: ', ''], 1)[0] + titles[x]
            body = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                    Ut a interdum tortor, varius ultricies neque. Maecenas \
                    blandit nisi rhoncus blandit blandit. Donec lacinia nisi \
                    vel nunc aliquam sodales. Phasellus auctor gravida eros, \
                    imperdiet mattis est luctus eget. Mauris quis rutrum ligula.'
            msg = Message(sender.id, receiver.id, subject, body)
            db.session.add(msg)
            db.session.commit()

    except Exception, e:
        print e
        print 'An user error has occured.'

    print 'messages have been seeded'


seed_data()
