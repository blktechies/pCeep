import urlparse
import oauth2 as oauth

from app import app

import json

twitter = app.config.get('SOCIAL_KEYS')['twitter']

consumer_key      = twitter['consumer_key']
consumer_secret   = twitter['consumer_secret']
request_token_url = twitter['request_token_url']
access_token_url  = twitter['access_token_url']
authorize_url     = twitter['authorize_url']
callback_url      = twitter['callback_url']
userinfo_url      = twitter['userinfo_url']

consumer = oauth.Consumer(consumer_key, consumer_secret)


def auth_url():
    client = oauth.Client(consumer)
    res, data = client.request(request_token_url, "POST")

    if res['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(data))
    token   = request_token['oauth_token']
    secret  = request_token['oauth_token_secret']
    confirm = request_token['oauth_callback_confirmed']
    auth_url= "%s?oauth_token=%s&oauth_token_secret=%s\
                &oauth_callback_confirmed=%s" % (authorize_url, 
                                                    token, 
                                                    secret, 
                                                    confirm)
    return dict(oauth_token=token, oauth_token_secret=secret, url=auth_url)


def req_access_token(oauth_token, oauth_token_secret, oauth_verifier):
    token = oauth.Token(oauth_token, oauth_token_secret)
    token.set_verifier(oauth_verifier)
    token.set_callback(callback_url)
    client = oauth.Client(consumer, token)
    res, data = client.request(access_token_url, "POST")
    return dict(urlparse.parse_qsl(data))


def req_userinfo(params):
    token = oauth.Token(params['oauth_token'], params['oauth_token_secret']) 
    username = params['screen_name']
    client = oauth.Client(consumer, token)
    info_url = "%s?screen_name=%s" %(userinfo_url, username)
    res, data = client.request(info_url)
    return data

def get_data(request):
    oauth_token = request.args.get('oauth_token')
    oauth_token_secret = ''
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = req_access_token(oauth_token, 
                                    oauth_token_secret, 
                                    oauth_verifier)
    rslts   = json.loads(req_userinfo(access_token))
    avatar  = rslts['profile_image_url_https'].replace('_normal', '')
    return dict(network          = 'twitter',
                    name            = rslts['name'], 
                    username        = rslts['screen_name'],
                    network_id      = rslts['id_str'],
                    profile_image   = avatar,
                    network_url     = 'https://%s/%s' %('twitter.com', 
                                                    rslts['screen_name']))