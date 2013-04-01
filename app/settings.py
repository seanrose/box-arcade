import os

BASE_URL = 'https://www.box.com/api/oauth2'
# If you're running it locally, we just set a random secret key
SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

# Get Box client credentials here: http://box.com/developers/services/edit/
BOX_CLIENT_ID = 'lyk5wlgetcan0ur7x15pzg9ekvh9p02k'
BOX_CLIENT_SECRET = 'zYLZ3FYBWOgzUkApoGsH3HOAKRLicJcu'
