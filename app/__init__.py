import os
import urllib
import settings
from box import BoxAuth
from itsdangeroussession import ItsdangerousSessionInterface
from flask import Flask, redirect, session, request, url_for, render_template

app = Flask(__name__)
os.environ['BOX_CLIENT_ID'] = settings.BOX_CLIENT_ID
os.environ['BOX_CLIENT_SECRET'] = settings.BOX_CLIENT_SECRET


def set_tokens_in_session(box_auth):
    session['access_token'] = box_auth.access_token,
    session['refresh_token'] = box_auth.refresh_token


def set_client_credentials_in_session(client_id, client_secret):
    session['client_id'] = client_id
    session['client_secret'] = client_secret


def get_client_credentials():
    client_id = session.get('client_id') or os.environ.get('BOX_CLIENT_ID')
    client_secret = (
        session.get('client_secret') or os.environ.get('BOX_CLIENT_SECRET')
    )
    return client_id, client_secret


@app.route('/')
def show_tokens():
    # If there are no tokens set on the session, show the modal to enter
    # client credentials
    if not session.get('access_token') or not session.get('refresh_token'):

        return render_template(
            'token.html',
            access_token='',
            refresh_token='',
            client_id='',
            show_modal=True,
            show_base_url=request.args.get('dev')
        )

    box = BoxAuth(
        *get_client_credentials(),
        access_token=session.get('access_token'),
        refresh_token=session.get('refresh_token'),
        base_url=session.get('base_url')
    )
    box.refresh_tokens()
    set_tokens_in_session(box)

    return render_template(
        'token.html',
        access_token=box.access_token,
        refresh_token=box.refresh_token,
        client_id=box.client_id,
        base_url=session.get('base_url')
    )


@app.route('/box_auth')
def box_auth():
    box = BoxAuth(*get_client_credentials(), base_url=session.get('base_url'))

    try:
        box.authenticate_with_code(request.args.get('code'))
        set_tokens_in_session(box)
    except:
        print 'OAuth 2 Error: {}'.format(request.args)

    return redirect(url_for('show_tokens'))


@app.route('/set_client_credentials', methods=['GET', 'POST'])
def set_client_credentials():
    session.clear()

    # Set the client credentials in the session
    # If this is a GET, the credentials in the form
    # will both be None, so we default to the credentials
    # set as environment variables
    set_client_credentials_in_session(
        request.form.get('client_id'),
        request.form.get('client_secret')
    )

    if request.form.get('base_url'):
        base_url = 'https://{}.inside-box.net/api/oauth2'.format(
            request.form.get('base_url')
        )
    else:
        base_url = None

    # Set the base_url in the session, if there was no base_url
    # in the form, we're ok because we only access the session
    # through dict.get()
    session['base_url'] = base_url

    redirect_uri = request.url_root + 'box_auth'

    # If we are on a local machine, we can't do https
    if '0.0.0.0:5000' not in redirect_uri:
        redirect_uri = redirect_uri.replace('http://', 'https://')

    box = BoxAuth(*get_client_credentials(), base_url=base_url)
    return redirect(box.get_authorization_url(
        redirect_uri=urllib.quote_plus(redirect_uri))
    )


@app.route('/logout')
def logout():
    # Revoke current tokens, if there are any
    box = BoxAuth(
        *get_client_credentials(),
        access_token=session.get('access_token'),
        refresh_token=session.get('refresh_token'),
        base_url=session.get('base_url')
    )
    box.revoke_tokens()

    # Clear everything out of the session
    session.clear()

    return render_template('logged_out.html')
