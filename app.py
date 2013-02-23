import os
from box import BoxAuth
from itsdangeroussession import ItsdangerousSessionInterface
from flask import Flask, redirect, session, request, url_for

app = Flask(__name__)


def set_tokens_in_session(box_auth):
    session['box_auth'] = {
        'access_token': box_auth.get_access_token(),
        'refresh_token': box_auth.get_refresh_token()
    }


@app.route('/')
def user_info():
    if not session.get('box_auth'):
        box = BoxAuth(os.environ.get('BOX_CLIENT_ID'),
                      os.environ.get('BOX_CLIENT_SECRET'))
        return redirect(box.get_authorization_url())

    box = BoxAuth(os.environ.get('BOX_CLIENT_ID'),
                  os.environ.get('BOX_CLIENT_SECRET'),
                  access_token=session.get('box_auth').get('access_token'),
                  refresh_token=session.get('box_auth').get('refresh_token'))

    box.refresh_tokens()
    set_tokens_in_session(box)

    return """
    <p><strong>Access Token:</strong> {}</p>
    <p><strong>Refresh Token:</strong> {}</p>
    <p><a href="/logout">logout</a></p>
    """.format(box.get_access_token(),
               box.get_refresh_token())


@app.route('/box_auth')
def box_auth():
    box = BoxAuth(os.environ.get('BOX_CLIENT_ID'),
                  os.environ.get('BOX_CLIENT_SECRET'))

    box.authenticate_with_code(request.args.get('code'))

    set_tokens_in_session(box)

    return redirect(url_for('user_info'))


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
    app.debug = True
    app.session_interface = ItsdangerousSessionInterface()
    app.secret_key = os.environ['SECRET_KEY']
    app.run(host='0.0.0.0', port=port)
