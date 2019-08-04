
# heroku URL: https://fbapp0111.herokuapp.com/

# access environment variables via dotenv library: https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv
from pathlib import Path  # python3 only

import os
import sqlalchemy

import json
from flask import g, Flask, flash, jsonify, redirect, render_template, request, session, make_response, Response
from flask_session import Session

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

from helpers import login_required, extend, get_page_access_token
import psycopg2 # import to use postgreSQL as database in python applications

# import libraries to force HTTPS redirect
from flask_sslify import SSLify

from bs4 import BeautifulSoup # webscraper

#from send_sms import send_sms
from scraper import scraper

from datetime import datetime, timedelta
from random import randint

import facebook # helps with facebook login
from facebook import get_user_from_cookie, GraphAPI

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from facebook_business.exceptions import FacebookError, FacebookRequestError
from facebook_business.adobjects.leadgenform import LeadgenForm
from facebook_business.adobjects.lead import Lead
from facebook_business.adobjects.leadgenformpreviewdetails import LeadGenFormPreviewDetails
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.adobjects.user import User

# set path to environment variables
env_path = Path('.gitignore') / '.env'
load_dotenv(dotenv_path=env_path)

# set app secret and app id
FB_APP_SECRET = os.getenv("APP_SECRET")
FB_APP_ID = os.getenv("APP_ID")  # (!)be sure to also change the app id in layout.html file

# acess the app's heroku database locally
# references: https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python; https://stackoverflow.com/questions/45133831/heroku-cant-launch-python-flask-app-attributeerror-function-object-has-no
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
sslify = SSLify(app)

'''the goal is to store a g.user in client storage; then, we can use if g.user throughout app to determine if we have valid access_token for user'''
@app.before_request
def get_current_user():

    print("start")

    if session.get("id") is not None:

        # Set the user in the session dictionary as a global g.user and bail out
        # of this function early.
        if session.get("user"):
            print("revisit")
            g.user = session.get("user")
            print(g.user)
            print("got g.user from session[user]!")
            return

        # Attempt to get the short term access token for the current user.
        result = get_user_from_cookie(
            cookies=request.cookies, app_id=FB_APP_ID, app_secret=FB_APP_SECRET
        )
        print("result: " + str(result))
        # result: none - means there are no cookies from fb so user is not logged into fb

#?      # see if user already has access_token for elif statement below
        #rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["id"])

        # if there is no result, we assume the user is not logged into facebook
        if result:
            print("logged in")

            # Check to see if there is already a row in database with that  user is already in FB by using result from cookie parsing
            # test id is '1139085602941741'
            user = db.execute("SELECT * FROM users WHERE user_id = :uid", uid = result["uid"])
            if user: # can delete when I understand more fully
                print("fb id in db: ")
                print(result["uid"])

            # user's fb id is not in db so get thier fbid and access token and add to the row associated with their app id
            if not user:
                print("first fb login")
                graph = GraphAPI(result["access_token"])
                profile = graph.get_object("me")
                if "link" not in profile:
                    profile["link"] = ""

                # update database entry that exists for currently logged in user to store their fb info
                #if session.get('id'):
                db.execute("UPDATE users SET user_id = :uid, access_token = :access, profile_url = :profile, name = :name WHERE id = :id",
                           uid=str(profile["id"]), access=result["access_token"], profile=profile["link"], name = profile["name"], id = session["id"]) # returns unique "id" of the user

            elif user[0]["access_token"] != result["access_token"]:
            # fb user is already in fb but new access_token does not match with one on file, so update
                print("app user, " + str(session["id"])  + ", HAS logged in w/ fb before but access_token is old so we've updated")

                # If an existing user, update the access token
                print("old access token: " + str(user[0]["access_token"]))
                print("new access token: " + str(result["access_token"]))

                # extend new access token
                result["access_token"] = extend(result["access_token"], FB_APP_ID, FB_APP_SECRET)

                db.execute("UPDATE users SET access_token = :access WHERE id = :id",
                                   access=result["access_token"], id = session["id"])

            # else if statement to handle users with multiple app accounts (i.e. have many rows in db)

            # store user in session
            #if user:
            # select the user based on app_id so we can add them to a session
            user = db.execute("SELECT * FROM users WHERE id = :app_id", app_id = session["id"])

            session["user"] = dict(
                name=user[0]["name"],
                profile_url=user[0]["profile_url"],
                user_id=user[0]["user_id"],
                access_token=user[0]["access_token"],
            )

        # If there is no result, we check if user is logging in from new computer
        '''
        elif rows[0]['access_token'] != None:
            print("inside user has an account and is on new device")
            session["user"] = dict(
                name=rows[0]["name"],
                profile_url=rows[0]["profile_url"],
                user_id=rows[0]["user_id"],
                access_token=rows[0]["access_token"],
            )
        '''
        # we assume the user is not logged in and set g.user to None or log in and set equal to user
        g.user = session.get("user", None)
        print(g.user)

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

        # Remember which user has logged in via sessions
        session["id"] = rows[0]["id"]
        print("id: " + str(session["id"]))

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

# get page_access_token to user during ad creation?

@app.route("/lead_ad_generator", methods=["GET", "POST"])
@login_required
def lead_ad_generator():
    print("inside lead_ad_generator")

    rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["id"])

    # if user does not have a valid access token, redirect to facebook login page; othwerise, launch lead_ad_generator
    # if there is no access token, user has not logged in
    if not g.user:
        print("no 'acess_token' found during call to lead_ad_generator method")
        return render_template("fblogin.html", app_id=FB_APP_ID)
    else:

        # create object and pass access_token and latest version as parameters
        FacebookAdsApi.init(access_token=g.user['access_token'], api_version='v3.3')

        # Get users pages
        fields = [
            'name',
        ]
        params = {
        }
        pages = User(g.user['user_id']).get_accounts(
          fields=fields,
          params=params,
        )
        page_count = len(pages)

        # get users ad accounts
        FacebookAdsApi.init(access_token=g.user['access_token'], api_version='v3.3')
        fields = [
            'name',
        ]
        params = {
        }
        ad_accounts = User(g.user['user_id']).get_ad_accounts(  # assuming id is the user_id
          fields=fields,
          params=params,
        )
        ad_account_count = len(ad_accounts)

        return render_template("lead_ad_generator.html", user=g.user, pages=pages, adaccounts=ad_accounts, ad_account_count=ad_account_count, page_count=page_count)

# get_location from user inputted string
# see get_valid_location.py for reference
@app.route('/get_locations', methods=['POST'])
def get_location():
    location_query = request.form['location_query']

    # reference: https://developers.facebook.com/docs/marketing-api/targeting-search#geo
    params = {
        'q': location_query,
        'type': 'adgeolocation',
        'location_types': ['city'], # only city results
        'limit': 5,
        "country_code": "US", # only search results from US
    }
    FacebookAdsApi.init(access_token=g.user['access_token'], api_version='v3.3')
    data = TargetingSearch.search(params=params)

    list = []
    for i in range(len(data)):
        #{'name':"Charleston, SC, United States", 'type': 'city'}
        str = data[i]["name"] + ", " + data[i]["region"] + ", " + data[i]["country_code"]
        list.append({'name' : str, 'type': data[i]["type"], 'key' : data[i]["key"]})

    return jsonify(list)

@app.route('/get_preview', methods=['POST'])
def get_preview():

    # gather all necessary variables
    ad_account = request.form['ad_account']
    page = request.form['page']
    headline = request.form['headline']
    text = request.form['text']
    privacy_policy = request.form['privacy_policy']
    url = request.form['url']
    budget = request.form['budget']
    image_url = request.form['image']

    # generate preview
    # reference on generating an ad preview from a non-existing ad: https://developers.facebook.com/docs/marketing-api/generatepreview/v3.2
    params_object = {
        'object_story_spec': { # https://developers.facebook.com/docs/marketing-api/reference/ad-creative-object-story-spec/
            'page_id': page,
            'link_data': { # https://developers.facebook.com/docs/marketing-api/reference/ad-creative-link-data/
                'message': text,
                'link': url, # must be same as 'link' in 'CTA' below
                #'image_hash': images[0]["hash"],
                'picture': image_url,
                'name': headline,
                'call_to_action': { # https://developers.facebook.com/docs/marketing-api/reference/ad-creative-link-data-call-to-action/
                    'type':'LEARN_MORE',
                    'value': {
                        'link': url,
                    }
                }
            }
        },
    }
    params = {
        'creative': params_object, # how to use a creative spec? https://developers.facebook.com/docs/marketing-api/reference/ad-creative
        'ad_format': 'MOBILE_FEED_STANDARD',
        }
    data = AdAccount(ad_account).get_generate_previews(params=params)

    # now that we have the ad preview, get <iframe> to display on html page
    soup = BeautifulSoup(data[0]['body'], 'html5lib')
    iframe = soup.find_all('iframe')[0]['src']
    return jsonify({'iframe' : iframe})

# given the relevant values, publish a lead ad to a user selected ad account and page
@app.route('/publish_ad', methods=['POST'])
def publish_ad():
#publish_ad.py is the definitive workflow for any questions regarding the publish_ad method
    try:
        # edge case to determine if page has leadgen_tos_accepted
        # reference leadgen_tos_accepted.py for questions
        page_id = request.form['page'] # '218711598949970' # abc realty
        FacebookAdsApi.init(access_token=g.user['access_token'], api_version='v3.3')
        result = Page(page_id).api_get( # api_get is the way to get a field from an object
            fields=['access_token'],
            params={},
        )
        page_access_token = result['access_token']

        # get leadgen_tos_accepted from marketing api
        FacebookAdsApi.init(access_token=page_access_token, api_version='v3.3')
        leadad_tos_accepted = Page(page_id).api_get( # api_get is the way to get a field from an object
            fields=['leadgen_tos_accepted'],
            params={},
        )

        if leadad_tos_accepted['leadgen_tos_accepted'] is False:
            return jsonify({'tos_accepted' : False})

        # initialize variables used during ad creation
        # ad_account = 'act_804097463107225' #hardcode to prevent publishing to bobs account # request.form['ad_account'] # set ad_account equal to user selected ad_account
        ad_account = request.form['ad_account'] # set ad_account equal to user selected ad_account
        url = request.form['url']
        privacy_policy = "https://fbapp0111.herokuapp.com/terms"  # what if app users could all use the same privacy policy that I host on the app
        message = request.form['text']
        headline = request.form['headline']
        budget = request.form['budget']
        image_url = request.form['image']
        city = request.form['city_key']
        print(ad_account)
        print(url)
        print(privacy_policy)
        print(message)
        print(headline)
        print(budget)
        print(image_url)
        print(city)

        # Step 1: create a campaign;
        # Here's a reference for campaign creation: https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#Creating

        fields = [
        ]
        params ={
            'name': "Campaign Name Placeholder",
            'objective': 'LEAD_GENERATION',
            'status': "PAUSED", # need to switch to active
            'buying_type': "AUCTION",
        }
        campaign = AdAccount(ad_account).create_campaign(
            fields=fields,
            params=params,
        )
        #session['lead_ad']['campaign_id'] = campaign["id"]  # save campaign id in session

    # Step 2: create an ad set
    # here's a reference: https://developers.facebook.com/docs/marketing-api/reference/ad-account/ad_sets/
    # https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group/adsets/

        fields = [
        ]
        params = {
          'name': "Ad Set Name Placeholder",
          'optimization_goal': 'LEAD_GENERATION',
          'billing_event': 'IMPRESSIONS',
          'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
          'lifetime_budget': budget, # $1
          'end_time' : datetime.now() + timedelta(days=3),
          'campaign_id': campaign["id"],
          "targeting": {
            "age_max": 65,
            "age_min": 18,
            "exclusions": {
              "interests": [
                {
                  "id": "6003278963980",
                  "name": "Loan officer"
                }
              ],
              "work_positions": [
                {
                  "id": "1025100880851927",
                  "name": "Real Estate Agent/Broker"
                },
                {
                  "id": "111867022164671",
                  "name": "Real estate broker"
                },
                {
                  "id": "171815889531702",
                  "name": "Real Estate Agent/Salesperson"
                }
              ]
            },
            "flexible_spec": [
              {
                "interests": [
                  {
                    "id": "1661352784116422",
                    "name": "Realtor.com"
                  },
                  {
                    "id": "6002925289859",
                    "name": "realtor.com"
                  },
                  {
                    "id": "6003174415534",
                    "name": "First-time buyer"
                  },
                  {
                    "id": "6003307244821",
                    "name": "Trulia"
                  },
                  {
                    "id": "6003496612657",
                    "name": "Homes.com"
                  },
                  {
                    "id": "6003909817136",
                    "name": "Zillow"
                  },
                  {
                    "id": "6003970928096",
                    "name": "House Hunting"
                  },
                  {
                    "id": "6015042704805",
                    "name": "trulia real estate"
                  }
                ]
              }
            ],
            "geo_locations": {
              "location_types": [
                "home",
                "recent"
              ],
              'cities':[{'key':city,'radius':15,'distance_unit':'mile'}]

            },
            "publisher_platforms": [
              "facebook"
            ],
            "facebook_positions": [
              "feed"
            ],
            "device_platforms": [
              "mobile"
            ]
          },
          'status': 'ACTIVE',
          'promoted_object': {'page_id': page_id},
        }
        ad_set = AdAccount(ad_account).create_ad_set(
          fields=fields,
          params=params,
        )

    # Step 3: create a form;
    # here's a reference document: https://developers.facebook.com/docs/marketing-api/guides/lead-ads/create
    # for a list of pre-fill questions, expand the questions parameter here: https://developers.facebook.com/docs/graph-api/reference/page/leadgen_forms/#Creating

        fields = [
        ]
        params = {  #  these fields can be found in under the page reference: https://developers.facebook.com/docs/graph-api/reference/page/
          'name': str(datetime.now()), # name must be unique so just use current date and time
          'follow_up_action_url': url,
          # 'question_page_custom_headline': "Form Question_Page_ Placeholder"'question page title',
          'questions': [
              {
                "key": "full_name",
                "type": "FULL_NAME",
              },
              {
                "key": "email",
                "type": "EMAIL",
              },
              {
                "key": "phone",
                "type": "PHONE",
              },
              ],
          #'privacy_policy_url': "https://fbapp0111.herokuapp.com/terms",
          #'privacy_policy': 'Object',
          'privacy_policy': {'url': privacy_policy, 'link_text': 'Privacy.'}, # https://developers.facebook.com/docs/graph-api/reference/page/
          #'legal_content_id': 'string',
          # thank_you_page is optional
         # "leadgen_tos_accepted": True
            }

        #FacebookAdsApi.init(access_token=session['page_access_token'])
        lead_gen_form = (Page(page_id).create_lead_gen_form( # ABC realty  page_id: 218711598949970 shaw marketing page_id: #1775351279446344
          fields=fields,
          params=params,
        ))

    # Step 4: create a creative
        fields = [
        ]
        params = {
            'object_story_spec': {
                'page_id': page_id,
                'link_data': {
                    'message': message,
                    'link': 'http://fb.me/',
                    'picture': image_url,
                    'name': headline,
                    #'caption':'WWW.ITUNES.COM',
                    #'description':'The link description',
                    #'title': adheadline,
                    'call_to_action': {
                        'type':'LEARN_MORE', # other options, include: APPLY_NOW, DOWNLOAD, GET_QUOTE, LEARN_MORE, SIGN_UP, SUBSCRIBE
                        'value': {
                            'link':'http://fb.me/',
                            'lead_gen_form_id': lead_gen_form['id']
                        }
                    }
                }
            },
        }
        #print(g.user['access_token'])
        #FacebookAdsApi.init(access_token=g.user['access_token']) # requires user access token
        creative = AdAccount(ad_account).create_ad_creative( # requires user access token
          fields=fields,
          params=params,
        )

    # Step 5: create an ad, which requires the creative_id and adset_id
        fields = [
        ]
        params = {
          'name': 'Ad Name Placeholder',
          'adset_id': ad_set["id"],
          'creative': {'creative_id': creative["id"]},
          'status': 'ACTIVE',
        }
        ad = AdAccount(ad_account).create_ad(
          fields=fields,
          params=params,
        )
        error = ""
        return jsonify({'error' : error})  # return facebook-specific error message if there is one
    except FacebookError as e:
        error = "Whoops! Error Publishing The Ad."
        if e.body():
            error = e.body()
            error = error['error']['error_user_msg']
        return jsonify({'error' : error})  # return facebook-specific error message if there is one

@app.route('/set_email', methods=['POST'])
def set_email():

    # add email to database
    email = request.form.get("email") # get email address entered
    print(email)
    print(session["id"]) # confirm we have a user
    db.execute("UPDATE users SET email = :email WHERE id = :id", email = email, id = session["id"])
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    # return apology(e.name, e.code)
    # return redirect('/error')
    return "error"


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get('PORT', 5000))
    # production mode
    app.run(host='0.0.0.0', port=port)

    # development mode
    #app.run(ssl_context='adhoc', host='0.0.0.0', port=port) # development mode
