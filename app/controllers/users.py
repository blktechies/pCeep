from flask import flash, g, redirect, render_template, request, url_for, session
from flask.ext.login import login_user, logout_user, current_user
from sqlalchemy import exc, desc

from app import app, db
from app.models import Description, User, SocialUser
from app.views import ProfileForm, WelcomeForm

from auth import twitter, github, linkedin
import utils


def get_user(id):
    id = unicode(int(id))
    return User.query.get(id)


def get_description(id):
    id = unicode(int(id))
    return Description.query.get(id)


def get_users():
    rslts = User.query.all()
    users = []
    for user in rslts:
        user.description = get_description(user.description_id).title
        users.append(user)
    return users


def get_descriptions():
    return Description.query.all()


def get_user_socialinfo(user):
    rslts = user.social_handles.all()
    info = {}
    for x in rslts:
        info[x.network] = x.username
    return info


def get_user_by_handle(handle):
    user = User.query.filter_by(handle = handle).first()
    if user:
        user.description = Description.query.get(user.description_id)
    return user

def gen_dict_from_params(params):
    return dict(network         = params.get('network'),
                name            = params.get('name'), 
                username        = params.get('screen_name'),
                network_id      = params.get('id_str'),
                profile_image   = params.get('profile_image'),
                network_url     = params.get('network_url'))


def gen_welcome_form(context):
    return WelcomeForm(network          = context['network'], 
                        name            = context['name'], 
                        username        = context['username'],
                        network_id      = context['network_id'],
                        profile_image   = context['profile_image'],
                        network_url     = context['network_url'])


def get_socialuser(network, network_id):
    return SocialUser.query.filter_by(network = network, network_id = network_id)


def get_or_create_socialuser(social_data, form):
    suser = get_socialuser(social_data['network'], social_data['network_id']).first()
    if(suser):
        if g.user.is_anonymous() == False:
            suser.user = g.user
            db.session.add(suser)
            db.session.commit()
            return redirect(url_for('get_profile_by_handle', handle = g.user.handle))
        else:
            try:
                login_user(get_user(suser.user_id))
                return redirect(request.args.get('next') or url_for('index')) 
            except TypeError:
                return render_template('welcome.html', form = form, context = social_data)
    else:
        suser = SocialUser(social_data.get('network'),
                            social_data.get('network_id'),
                            social_data.get('username'),
                            social_data.get('network_url'))
        if g.user.is_anonymous() == False:
            suser.user = g.user
            db.session.add(suser)
            db.session.commit()
            return redirect(url_for('get_profile_by_handle', handle = g.user.handle))
        else:
            db.session.add(suser)
            db.session.commit()
            return render_template('welcome.html', form = form, context = social_data)


def get_or_create_user(params):
    user = User.query.filter_by(email = params.get('email'))
    if user.first():
        return 'exists'
    else:
        name = params.get('name')
        try:
            sugg_username = (name.split()[0] + name.split()[1]).lower()
        except:
             sugg_username = name.lower()   
        user = User(params.get('email'),
                    name,
                    params.get('profile_image'))
        db.session.add(user)
        db.session.commit()
        return user


def complete_user_setup(params):
    # ToDo: Dry this up
    context = gen_dict_from_params(params)
    form = gen_welcome_form(context)
    user = get_or_create_user(params)
    if user == 'exists':
        flash('Danger: Sorry, the email address %s already exists. We will shoot a \
                note to that addy to confirm you want to add this social \
                login to your account. Until then, maybe try one of your \
                other socal logins?' %(params.get('email')))
        return render_template('welcome.html', 
                                form = form, 
                                context = context)
    else:
        suser = get_socialuser(params.get('network'), 
                                params.get('network_id')).first()
        suser.user  = user
        db.session.add(suser)
        db.session.commit()
        login_user(user)
        return redirect(url_for('get_profile_by_handle', handle = g.user.handle))


def get_or_create_login(network):

    if network == 'twitter':
        context =  twitter.get_data(request)

    if network == 'github':
        if session['state'] == request.args['state']:
            context = github.get_data(request)
        else:
            return 'Bad request. Sneaky guy.'
        
    if network == 'linkedin':
        if session['state'] == request.args['state']:
            context = linkedin.get_data(request)
        else:
            return 'Bad request. Sneaky guy.'

    if g.user.is_anonymous() == False:
        return get_or_create_socialuser(context, gen_welcome_form(context))

    return get_or_create_socialuser(context, gen_welcome_form(context))
    

def gen_profle_form(params):
    return ProfileForm(user_id          = params.id,
                        handle          = params.handle,
                        display_name    = params.display_name,
                        email           = params.email,
                        status          = params.status)


def update_profile(params):
    user                = get_user(params['user_id'])
    curr_handle         = user.handle
    user.display_name   = params['display_name']
    user.handle         = params['handle']
    user.email          = params['email']
    user.status         = params['status']
    user.description_id = params['description']
    db.session.add(user)
    try:
        db.session.commit()
        handle      = user.handle
        message     = 'Success: Profile updated'

    except exc.IntegrityError, e:
        db.session.rollback()
        handle      = curr_handle
        message     = 'Danger: This %s is already taken. Please choose another.' \
                        % (str(e).split(' ')[2])
    flash(message)
    return redirect(url_for('get_profile_by_handle', handle = handle))



def logout():
    logout_user()
    return redirect(url_for('index'))


def internal_error():
    db.session.rollback()
    return render_template('500.html'), 500