import os
from app import app, settings
from app.itsdangeroussession import ItsdangerousSessionInterface

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.session_interface = ItsdangerousSessionInterface()
    app.secret_key = settings.SECRET_KEY
    app.run(host='0.0.0.0', port=port)
