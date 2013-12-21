#!/usr/bin/env python
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
import datetime
import os.path

from app import db
from app.models import  Description, SocialUser, User, Post, Interest, Comment, Comment_Reply
from app.controllers import utils

import random

import seed_data

descrips    = seed_data.DESCRIPTIONS
seeds       = seed_data.USERS
posts       = seed_data.POSTS
cmnts       = seed_data.COMMENTS
intrsts     = seed_data.INTERESTS

today = datetime.datetime.utcnow()
last_month = datetime.date(day=1, month=today.month, year=today.year) - datetime.timedelta(days=30)

def seed_data():
    try:
        for d in descrips:
            db.session.add(Description(d))
            db.session.commit()

        dbdescrips = Description.query.all()
        for el in seeds:
            date_created = utils.random_date(datetime.datetime(2013,01,01), 
                                            datetime.datetime(2013,12,05))
            # user accounts
            acct = seeds[el]['account']
            user = User( acct['email'],
                            acct['display_name'], 
                            acct['image_url'])
            user.handle = acct['handle']
            user.status = acct['status']
            user.description_id = random.sample(dbdescrips, 1)[0].id
            user.date_created = date_created
            user.last_seen = utils.random_date(date_created, 
                                                datetime.datetime.utcnow())
            db.session.add(user)
            db.session.commit()

            interests = random.sample(intrsts, random.randrange(2, 7))
            for speciality in interests:
                db.session.add(Interest(user.id, speciality))
                db.session.commit()


            # social accounts
            social = seeds[el]['social']
            for ntwrk in social:
                sn = social[ntwrk]
                suser = SocialUser(sn['network'],
                                    sn['network_id'],
                                    sn['username'],
                                    sn['network_url'])
                db.session.add(suser)
                suser.user = User.query.filter_by(display_name = acct['display_name']).first()
                db.session.commit()
        
        try:
            # posts
            users = User.query.all()
            for i, val in enumerate(posts):
                user = users[i]
                post_date_created = utils.random_date(user.date_created, 
                                                      datetime.datetime.utcnow())
                post = Post(user.id, val['title'], val['body'])
                post.user = user
                post.date_created = post_date_created
                post.last_updated = utils.random_date(last_month, 
                                                        datetime.datetime.utcnow())
                db.session.add(post)
                db.session.commit()

            try:
                # comments
                dbposts = Post.query.all()
                def post_cmnt(user_id, post_id, body, 
                                datestamp = datetime.datetime.utcnow()):
                    comment = Comment(user_id, post_id, body)
                    comment.date_created = datestamp
                    comment.last_updated = datestamp
                    db.session.add(comment)
                    db.session.commit()

                for post in dbposts:
                    for x in range(0, random.randrange(6)):
                        user = random.sample(users, 1)[0]
                        cmnt = random.sample(cmnts, 1)[0]
                        datestamp = utils.random_date(last_month, 
                                                        datetime.datetime.utcnow())
                        post_cmnt(user.id, post.id, cmnt, datestamp)


                # comment replies
                dbcmnts = Comment.query.all()
                def post_reply(user_id, cmnt_id, body,
                                datestamp = datetime.datetime.utcnow()):
                    reply = Comment_Reply(user_id, cmnt_id, body)
                    reply.date_created = datestamp
                    reply.last_updated = datestamp
                    db.session.add(reply)
                    db.session.commit()

                for c in dbcmnts:
                    for x in range(0, random.randrange(3)):
                        user = random.sample(users, 1)[0]
                        cmnt = random.sample(cmnts, 1)[0]
                        datestamp = utils.random_date(c.last_updated, 
                                                            datetime.datetime.utcnow())
                        post_reply(user.id, c.id, cmnt, datestamp)


            except Exception, e:
                print e
                print 'An comment error has occured.'
                return

        except Exception, e:
            print e
            print 'A content error has occured.'
            return

        print 'DB seeded with development data.'

    except Exception, e:
        print e
        print 'An user error has occured.'


seed_data()
