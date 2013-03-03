import os

BASE_URL = 'https://www.box.com/api/oauth2'
# If you're running it locally, we just set a random secret key
SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

# Get Box client credentials here: http://box.com/developers/services/edit/
BOX_CLIENT_ID = 'hs8k9gu30co0rx5htt91gs0xcevntaxp'
BOX_CLIENT_SECRET = 'QvTijDGniBGv7Jhk26teeS45D6do0nBH'
