from app.controllers import utils
from httplib2 import Http
from urllib import urlencode

import json

from app import app


linkedin = app.config.get('SOCIAL_KEYS')['linkedin']

api_key             = linkedin['api_key']
secret_key          = linkedin['secret_key']
access_token_url    = linkedin['access_token_url']
authorize_url       = linkedin['authorize_url']
redirect_uri        = linkedin['redirect_uri']
callback_url        = linkedin['callback_url']
scope               = linkedin['scope']
userinfo_url        = linkedin['userinfo_url']
fields              = linkedin['fields']
state               = utils.random_str(20)


def auth_url():
    url = '%s?response_type=code&client_id=%s&scope=%s&state=%s&redirect_uri=%s' \
            % (authorize_url, api_key, scope, state, redirect_uri)
    return dict(url = url, state = state)


def req_access_token(request):
    headers = { "Accept": "application/json" };
    params = dict(grant_type        ='authorization_code',
                    code            = request.args['code'],
                    redirect_uri    = redirect_uri,
                    client_id       = api_key, 
                    client_secret   = secret_key)
    token_url = '%s?%s' % (access_token_url , urlencode(params))
    res, rslts = Http().request(uri = token_url,
                                method = 'POST',
                                headers = headers)
    return json.loads(rslts)['access_token']


def req_userinfo(params):
    headers = { "Accept": "application/json" };
    data_url = userinfo_url + ':('+fields+')?format=json&oauth2_access_token=' \
                            + params
    res, rslts = Http().request(uri = data_url, headers = headers)
    return rslts


def get_data(request):
    access_token = req_access_token(request)
    rslts   = json.loads(req_userinfo(access_token))
    data    = dict(network          = 'linkedin',
                    name            = '%s %s' % (rslts['firstName'], rslts['lastName']),
                    username        = rslts['publicProfileUrl'].split('/')[4],
                    network_id      = rslts['id'],
                    network_url     = rslts['publicProfileUrl'])
    try:
        pic_url = userinfo_url + '/picture-urls::(original)?format=json&oauth2_access_token=' \
                            + acc_rslts['access_token']
        pic_res, pic_rslts = client.request(uri = data_url, headers = headers)
        data['profile_image'] = pic_rslts['picture-urls']
    except:
        data['profile_image'] = utils.avatar(rslts['emailAddress'], 150)
    return data