import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY = '53hd+umt@*qxmx(c5y33eezoi#qs1el%j9n6v-374nbe_)$b00muiral'

SOCIAL_KEYS = {
    'twitter': {
        'consumer_key'      : 'Xw8ruTX0GSqfwHBfzskjg',
        'consumer_secret'   : 'aUGNSJub1uxT9PzmgzmpfZfeSfAgJLTREDzW4M',
        'request_token_url' : 'https://api.twitter.com/oauth/request_token',
        'access_token_url'  : 'https://api.twitter.com/oauth/access_token',
        'authorize_url'     : 'https://api.twitter.com/oauth/authorize',
        'redirect_uri'      : 'http://127.0.0.1:5000',
        'callback_url'      : 'http://127.0.0.1:5000/auth/twitter',
        'verify_cresentials': 'https://api.twitter.com/1.1/account/verify_credentials.json',
        'userinfo_url'      : 'https://api.twitter.com/1.1/users/show.json'
    },
    'github': {
        'client_id'         : '0a8f9f1606eb8bf5bfc4',
        'client_secret'     : '064b18ea4fa2a047baeb7e9c7affca1eaec0bfd4',
        'authorize_url'     : 'https://github.com/login/oauth/authorize',
        'access_token_url'  : 'https://github.com/login/oauth/access_token',
        'redirect_uri'      : 'http://127.0.0.1:5000/auth/github',
        'callback_url'      : 'http://127.0.0.1:5000',
        'userinfo_url'      : 'https://api.github.com/user',
        'scopes'            : 'user'
    },
    'linkedin': {
        'api_key'           : '77brlp68poky60',
        'secret_key'        : '4QrmbfokgnBuwd6Q',
        'access_token_url'  : 'https://www.linkedin.com/uas/oauth2/accessToken',
        'authorize_url'     : 'https://www.linkedin.com/uas/oauth2/authorization',
        'callback_url'      : 'http://127.0.0.1:5000',
        'redirect_uri'      : 'http://127.0.0.1:5000/auth/linkedin',
        'userinfo_url'      : 'https://api.linkedin.com/v1/people/~',
        'scope'             : 'r_basicprofile r_emailaddress',
        'fields'            : 'id,first-name,last-name,picture-url,public-profile-url,email-address'
    }
}