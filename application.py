
# heroku URL: https://fbapp0111.herokuapp.com/


# access environment variables via dotenv library: https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv
from pathlib import Path  # python3 only

import os
import sqlalchemy

from flask import g, Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# from flask_talisman import Talisman
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

try:  # try python 3 first
    import urllib
    from urllib.parse import urlparse
except ImportError:  # else revert to python 2
     from urlparse import urlparse
#import urllib.parse

from helpers import apology, login_required, extend
import psycopg2 # import to use postgreSQL as database in python applications

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.leadgenform import LeadgenForm
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.lead import Lead
from facebook_business.adobjects.leadgenformpreviewdetails import LeadGenFormPreviewDetails
import facebook
from facebook import get_user_from_cookie, GraphAPI

from flask_sslify import SSLify
from bs4 import BeautifulSoup # webscraper

#from send_sms import send_sms
from scraper import scraper

from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.api import FacebookAdsApi


from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.page import Page

from random import randint

# set path to environment variables
env_path = Path('.gitignore') / '.env'
load_dotenv(dotenv_path=env_path)

# set app secret and app id
FB_APP_SECRET = os.getenv("DEV_APP_SECRET_TEST")
FB_APP_ID = os.getenv("DEV_APP_ID")  # (!)be sure to also change the app id in layout.html file

# acess the app's heroku database locally
# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
# https://stackoverflow.com/questions/45133831/heroku-cant-launch-python-flask-app-attributeerror-function-object-has-no
urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.getenv("DATABASE_URL"))
db = SQL(os.environ["DATABASE_URL"]) # os.environ["APP_SECRET"]

# Configure app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# encrypt session storage
app.secret_key = os.urandom(24) # https://www.youtube.com/watch?v=T1ZVyY1LWOg

# initiate a flask session dictionary
Session(app)

@app.before_request
def get_current_user():
    """Set g.user to the currently logged in user.
    Called before each request, get_current_user sets the global g.user
    variable to the currently logged in user.

    A currently logged in user is determined by seeing if it exists in Flask's session dictionary.
        If it is the first time the user is logging into this application it will create the user and insert it into the database.
    If the user is not logged in, None will be set to g.user.
    """

    print("At start of get_current_user method")

    # Set the user in the session dictionary as a global g.user and bail out
    # of this function early.
    if session.get("user"):
        print("inside of session.get(user)")
        g.user = session.get("user")
        if session.get('id'):
            print("id: " + str(session["id"]))
            db.execute("INSERT INTO users (access_token) VALUES (:access) WHERE user_id = :uid", access=session["user"]["access_token"], uid = session["user"]["id"])
        print("end get_current_user early b/c there is a user in session")
        return

    # Attempt to get the short term access token for the current user.
    result = get_user_from_cookie(
        cookies=request.cookies, app_id=FB_APP_ID, app_secret=FB_APP_SECRET
    )

    # if there is no result, we assume the user is not logged into facebook
    if result:
        print("inside if result")

        # extend access token
        result["access_token"] = extend(result["access_token"], FB_APP_ID, FB_APP_SECRET)

        # Check to see if this Facebook user_id is already in our database.
        print("uid: " + str(result["uid"])) # facebook user id: 1139085602941741 <- business id? It's under business integerations
        user = db.execute("SELECT * FROM users WHERE user_id = :uid", uid = result["uid"])
        print("user: " + str(user)) # row 23

        # It's the 1st time user is logging in, so create a user and add them to current row in database by id
        if not user:
            print("inside if not user[0]")
            # Not an existing user so get info
            graph = GraphAPI(result["access_token"])
            profile = graph.get_object("me")
            if "link" not in profile:
                profile["link"] = ""

            # Create the user and insert it into the database
            #print("profile_url: " + profile["link"])
            #print("profile_id: " + str(profile["id"]))
            #print("name: " + str(profile["name"]))
            if session.get('id'):
                print("id: " + str(session["id"]))
                db.execute("UPDATE users SET user_id = :uid, access_token = :access, profile_url = :profile, name = :name WHERE id = :id",
                               uid=str(profile["id"]), access=result["access_token"], profile=profile["link"], id = session["id"], name = profile["name"]) # returns unique "id" of the user
            #print("user: " + str(user))

        elif user[0]["access_token"] != result["access_token"]:
            print("inside user[0][accesstoken] != result[access_token]")

            # If an existing user, update the access token
            print("old access token: " + str(user[0]["access_token"]))
            print("new access token: " + str(result["access_token"]))
            db.execute("UPDATE users SET access_token = :access WHERE user_id = :uid",
                               access=result["access_token"], uid = result["uid"])
            # add existing facebook user (id and access code) to current logged in person using id or user_name
            print("old access token: " + str(user[0]["access_token"]))

        # Add the user to the current session
        if user:
            print("inside if user")
            session["user"] = dict(
                name=user[0]["name"],
                profile_url=user[0]["profile_url"],
                id=user[0]["user_id"],
                access_token=user[0]["access_token"],
            )

        # If there is no result, we assume the user is not logged in and set g.user to None
    # Commit changes to the database and set the user as a global g.user
    g.user = session.get("user", None)

    print("at end of get_current_user method")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    # session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Must provide username', 'error')
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Must provide password', 'error')
            return redirect("/register")

        # Ensure passwordConfirmation was submitted
        elif not request.form.get("confirmation"):
            flash('Passwords do not match', 'error')
            return redirect("/register")

        # check passwords equals password confirmation
        elif not request.form.get("password") == request.form.get("confirmation"):
            flash('Passwords do not match', 'error')
            return redirect("/register")

        # reject duplicate username
        result = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if result:
            flash('Username taken', 'error')
            return redirect("/register")
            # return apology("username taken", 200)

        # Hash password
        # https://www.programcreek.com/python/example/82817/werkzeug.security.generate_password_hash
        hashed_password = generate_password_hash(request.form.get("password"))

        # Store user + pass in database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=request.form.get("username"), hash=hashed_password)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Remember which user has logged in by adding id to session
        session["id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    # session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Must provide username', 'error')
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Must provide password', 'error')
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",  # returns an array
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Invalid Username and/or Password', 'error')
            return redirect("/login")

        # Remember which user has logged in via a global variable
        #global userId
        #id = rows[0]["id"]
        #print("userId: " + str(userId))

        # Remember which user has logged in via sessions
        session["id"] = rows[0]["id"]
        print("id: " + str(session["id"]))

        # need to access the first row of the array rows, row[0] and then go to the index cash, ["cash"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # remove user from the session
    session.pop("user", None)
    session.pop("id", None)

    # Redirect user to login form
    return redirect("/login")

@app.route("/")
@login_required
def index():
    if session.get("user"):
        message = "Get MORE Leads!!"
    else:
        message = "Get Leads!!"
    return render_template("index.html", message=FB_APP_ID)

@app.route("/create_lead_ad", methods=["GET", "POST"])
@login_required
def create_lead_ad():
    # set rows equal to current user row in 'users' table
    rows = db.execute("SELECT * FROM users WHERE id = :id",  # returns an array
                      id=session["id"])

    # if user does not have a valid access token, redirect to facebook login page
    if rows[0]["access_token"] is None:
        print("no 'acess_token' found during call to create_lead_ad method")
        return render_template("fblogin.html", app_id=FB_APP_ID)
    return "lead ad template goes here"

@app.route("/ads", methods=["GET", "POST"])
#@login_required
def ads():
    print("running ads method")
    if request.method == "POST":
        if request.form.get("campname"):
            flash('Must provide a Name for your Campaign and Adset', 'error')
            return render_template("ads.html")
        elif request.form.get("adsetname"):
            flash('Must provide a Name for your Campaign and Adset', 'error')
            return render_template("ads.html")
        else:
        #try:
            # get user inputs
            objective = request.form.get("objective")
            print(objective)
            campname = request.form.get("campname")
            print(campname)
            adsetname = request.form.get("adsetname")
            print(adsetname)
            adaccount = 'act_804097463107225'
            print(adaccount)

            #create campaign
            fields = [
            ]
            params ={
                'name': 'test campaign',
                'objective': 'LEAD_GENERATION',
                'status': "PAUSED",
            }
            newcampaign = AdAccount(adaccount).create_campaign(
                fields=fields,
                params=params,
            )
            print(newcampaign)

            session['adaccount'] = adaccount
            print(session['adaccount'])
            return redirect("/adresults")
    else:
        if not session.get("user"): # since user is not logged in, prompt them to login
            print("no 'session user' during call to ads method")
            return render_template("fblogin.html", app_id=FB_APP_ID)
        elif session.get("user"): # user is logged in
        #try:
            user_id = g.user['user_id']
            print("there is a 'session user' during the call to ads method")
            print(user_id)
            access_token = g.user['access_token']
            print(access_token)
            FacebookAdsApi.init(access_token=access_token)

            '''
            # get users ad accounts using the user_id and access_token above
            fields = [
                'name',
            ]
            params = {
            }
            adaccounts = (User(user_id).get_ad_accounts(  # assuming id is the user_id
              fields=fields,
              params=params,
            ))
            #id = adaccounts[0]["id"]
            #print("id")
            #print(id)
            count = len(adaccounts)
            print("rendering template ads.html")
            return render_template("ads.html", user=g.user, adaccounts=adaccounts, count=count)
            '''
            print("redirect from /ads to /preview")
            return redirect("/preview")


@app.route("/adresults", methods=["GET", "POST"])
#@login_required
def adresults():
    '''
    adaccount = session['adaccount'] # https://stackoverflow.com/questions/17057191/redirect-while-passing-arguments
    adpreview = session['adpreview'] # retrieved from /leadads
    soup = BeautifulSoup(adpreview, 'html5lib')
    iframe = soup.find_all('iframe')[0]['src']
    print(iframe)
    print(adaccount)
    '''
    adaccount = 'act_804097463107225'

    if request.method == "POST":
        pass
    else:
        if 1==1:
            fields = [ # see "adinsights.py" class "AdInsights" for fields since that's that the fxn references
              'campaign_name',
              'reach',
              'clicks',
              'spend',
              'account_id',
              'date_start',
              'date_stop',
              'campaign_id',
            ]
            params = { # /act_804097463107225/insights?fields=ad_id,impressions&date_preset=lifetime&level=ad
              'date_preset': 'lifetime',
              'level': 'campaign',
            }
            adsets = (AdSet(adaccount).get_insights( # https://developers.facebook.com/docs/marketing-api/insights
              fields=fields,
              params=params,
            ))

            print(adsets)
            count = len(adsets)

        return render_template("adresults.html", adsets=adsets, count=count)

@app.route("/terms", methods=["GET", "POST"])
def terms():
    print("##### terms/logout ######")
    session.pop("user", None)
    return render_template("terms.html", user=g.user)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

"""
# try for HTTPS on localhost
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
httpd = HTTPServer(('localhost', 4443), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='server_unencrypted.pem', server_side=True)
httpd.serve_forever()
"""

if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get('PORT', 5000))
    app.run(ssl_context='adhoc', host='0.0.0.0', port=port)

#if __name__ == '__main__':
#app.debug = False
#port = int(os.environ.get('PORT', 5000))  #getenv  # port = int(os.environ.get('PORT', 5000))
#app.run(host='0.0.0.0', port=port)
