import os
import urllib
from box import BoxAuth
from itsdangeroussession import ItsdangerousSessionInterface
from flask import Flask, redirect, session, request, url_for, render_template

app = Flask(__name__)


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
    if not session.get('access_token') or not session.get('refresh_token'):

        return render_template(
            'token.html',
            access_token='',
            refresh_token='',
            client_id='',
            show_modal=True
        )

    box = BoxAuth(
        *get_client_credentials(),
        access_token=session.get('access_token'),
        refresh_token=session.get('refresh_token')
    )
    box.refresh_tokens()
    set_tokens_in_session(box)

    return render_template(
        'token.html',
        access_token=box.access_token,
        refresh_token=box.refresh_token,
        client_id=get_client_credentials()[0]
    )


@app.route('/box_auth')
def box_auth():
    box = BoxAuth(*get_client_credentials())

    box.authenticate_with_code(request.args.get('code'))

    set_tokens_in_session(box)

    return redirect(url_for('show_tokens'))


@app.route('/set_keys')
def set_keys():
    session.clear()
    set_client_credentials_in_session(
        request.args.get('client_id'),
        request.args.get('client_secret')
    )
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
    redirect_uri = request.url_root + 'box_auth'

    # If we are on a local machine, we can't do https
    if '0.0.0.0:5000' not in redirect_uri:
        redirect_uri = redirect_uri.replace('http://', 'https://')

    box = BoxAuth(*get_client_credentials())
    return redirect(box.get_authorization_url(
        redirect_uri=urllib.quote_plus(redirect_uri))
    )


@app.route('/logout')
def logout():
    session.clear()
    return """
    <p>You are now logged out of your Box account.</p><br>
    <a href="/">log back in</a>
    """


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    # app.debug = True
    app.session_interface = ItsdangerousSessionInterface()
    app.secret_key = os.environ['SECRET_KEY']
    app.run(host='0.0.0.0', port=port)
