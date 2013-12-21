from app.controllers import utils
from httplib2 import Http
from urllib import urlencode

import json

from app import app


github = app.config.get('SOCIAL_KEYS')['github']

client_id           = github['client_id']
client_secret       = github['client_secret']
authorize_url       = github['authorize_url']
access_token_url    = github['access_token_url']
redirect_uri        = github['redirect_uri']
callback_url        = github['callback_url']
scopes              = github['scopes']
userinfo_url        = github['userinfo_url']
state               = utils.random_str(20)


def auth_url():
    url = '%s?client_id=%s&redirect_uri=%s&scopes=%s&state=%s' \
            % (authorize_url,client_id, redirect_uri, scopes, state)
    return dict(url = url, state = state)


def req_access_token(request):
    headers = { "Accept": "application/json" };
    params = dict(client_id         = client_id, 
                    client_secret   = client_secret, 
                    code            = request.args['code'])
    
    res, rslts = Http().request(uri     = access_token_url,
                                method  = 'POST',
                                headers = headers,
                                body    = urlencode(params))
    return json.loads(rslts)['access_token']


def req_userinfo(params):
    data_url = userinfo_url + '?access_token=' + params
    res, rslts = Http().request(data_url)
    return rslts


def get_data(request):
    access_token = req_access_token(request)
    rslts   = json.loads(req_userinfo(access_token))
    return dict(network          = 'github',
                    name            = rslts['name'], 
                    username        = rslts['login'],
                    network_id      = rslts['id'],
                    profile_image   = rslts['avatar_url'].split('d=')[0]+'s=200',
                    network_url     = rslts['url'])