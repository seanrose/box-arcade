box-arcade
===================

A Simple Flask App for generating and refreshing access tokens for [Box OAuth 2](http://developers.box.com/oauth/)

Live demo here: https://box-token-generator.herokuapp.com
*You shouldn't use production client credentials or login information with the demo–NEVER share your production client secret with anyone*

Installation
------------

1. Install [virtualenv](http://www.virtualenv.org/en/latest/#installation)

2. Clone the source code:

    `$ git clone https://github.com/seanrose/box-arcade.git`

3. cd into the directory you just cloned

	`$ cd box-arcade`

4. Create a virtual environment

	`$ virtualenv .env --distribute`

5. Activate the virtual environment

	`$ source .env/bin/activate`

6. Install the dependencies

	`$ pip install -r requirements.txt`

7. Start up the web server

	`$ python runserver.py`

8. Go to the now running app at [http://0.0.0.0:5000/](http://0.0.0.0:5000/)

9. Sign in and have fun with your tokens!

![](http://imgur.com/2T0UyMa.gif)
