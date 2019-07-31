
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

from helpers import apology, login_required, extend, get_page_access_token
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
        print("end get_current_user early b/c there is a user in session")
        return

    # Attempt to get the short term access token for the current user.
    result = None;
    if request.cookies:
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
                user_id=user[0]["user_id"],
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

# get page_access_token to user during ad creation

@app.route("/lead_ad_generator", methods=["GET", "POST"])
@login_required
def lead_ad_generator():
    # set rows equal to current user row in 'users' table
    rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["id"])

    # if user does not have a valid access token, redirect to facebook login page; othwerise, launch lead_ad_generator
    if rows[0]["access_token"] is None:
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

@app.route('/lead_ad_process_1', methods=['POST'])
def lead_ad_process_1():
    print("in /lead_ad_process_1")
    headline = request.form['headline']
    ad_account = request.form['ad_account']

    '''
    # given page id, determine page access token
    graph = GraphAPI(access_token=g.user['access_token'])
    data = graph.get_object("/" + str(ad_account) + "?fields=access_token") # get_object(self, id, **args):
    page_access_token = data['access_token']
    '''

    return jsonify({'headline' : headline, 'ad_account' : ad_account})


@app.route('/lead_ad_step_2', methods=['POST'])
def lead_ad_step_2():
    print("in /lead_ad_step_2")
    ad_account = request.form['ad_account']
    page = request.form['page']

    # generate preview src
    # hardcode so don't have to login
    user_access_token = session["user"]["access_token"]
    page_access_token = os.getenv("TEST_PAGE_ACCESS_TOKEN")
    FacebookAdsApi.init(access_token=page_access_token)

    print("inside /preview")

    # METHOD 2: generate an ad preview from a non-existing ad: https://developers.facebook.com/docs/marketing-api/generatepreview/v3.2
    # two steps: (1) create an object_story_spec and (2) use the gen_generate_previews function from the user's ad account node

    # get an image hash to use for ad by reading from ad accounts existing images
    account = AdAccount(ad_account)
    images = account.get_ad_images()

    params_object = {
        'object_story_spec': {
            'page_id': page,
            'link_data': {
                'message': "message",
                'link': 'http://fb.me/',
                'image_hash': images[0]["hash"], # two options to get hash: (1) upload an image or (2) read from existing images
                'name': "headline",
                #'caption':'WWW.ITUNES.COM',
                #'description':'The link description',
                #'title': adheadline,
                'call_to_action': {
                    'type':'LEARN_MORE',
                    'value': {
                        'link':'http://fb.me/',
                        #'lead_gen_form_id': lead_gen_form['id']
                    }
                }
            }
        },
    }
    params = {
        'creative': params_object, # how to use a creative spec? https://developers.facebook.com/docs/marketing-api/reference/ad-creative
        'ad_format': 'MOBILE_FEED_STANDARD',
        }
    FacebookAdsApi.init(access_token=g.user['access_token'], api_version='v3.3')
    data = AdAccount(ad_account).get_generate_previews(params=params)

    # now that we have the ad preview, get <iframe> to display on html page
    data = data[0]['body']
    soup = BeautifulSoup(data, 'html5lib')
    iframe = soup.find_all('iframe')[0]['src']
    print(iframe)

    # return src to html page
    return jsonify({'iframe' : iframe})

@app.route('/process', methods=['POST'])
def process():

    phone = request.form['phone']
    name = request.form['name']
    email = request.form['email']

    if name and email:
        newName = name[::-1]

        return jsonify({'name' : phone})

    return jsonify({'error' : 'Missing data!'})

'''
# add new info to API
@app.route('/process_2', methods=['POST'])
def process_1():
    print("in /process_2")
    headline = request.form['headline']
    print("headline: " + str(headline))
    lead_ad_preview = preview(); # set lead_ad_preview variable equal to return of preview() method
    return jsonify({'headline' : headline, 'lead_ad_preview' : lead_ad_preview})
'''

@app.route('/preview', methods=['GET'])
def preview():

    # hardcode so don't have to login
    user_access_token = session["user"]["access_token"]
    page_access_token = os.getenv("TEST_PAGE_ACCESS_TOKEN")
    FacebookAdsApi.init(access_token=page_access_token)

    print("inside /preview")

    # if user just typed in URL, run scraper
    if not request.form.get("budget"):
        print("running if not budget request")

        city = request.form.get('city')
        print(city)

        # add necessary values to dict -- added to database table as default
        ad_details = {
          "page_id": "1775351279446344",
          "adaccount_id": 'act_804097463107225',
          'adaccount_name': 'Justin Shaw',
            "lead_gen_form_id": "",
            "privacy_policy_url": "soldoncharleston.com/terms",
            "property_url": "soldoncharleston.com/property/19004415",
            "budget": 5,
            "duration": 3
        }


        # global testdict
        #property_details = scraper(request.form.get('query_address')) # call the scraper function with the query_address
        property_details = {
            'query_address': '1315 Center Lake Drive',   # request.form.get('query_address'),
            'query_city': 'MOUNT PLEASANT',  #request.form.get('query_city').upper(),
            'beds': '3',
            'baths': '2.5',
            'sqft': '1500',
            'price': '$400,000',
            'scraped_address': '1315 Center Lake Drive, Mount Pleasant, SC 29464',
            'scraped_image': 'https://t.realgeeks.media/thumbnail/LSsbogr5NtKyMMN5PUUqjiVv98w=/trim:top-left:50/https://property-media.realgeeks.com/101/40de1f38333c75fe778e90a32241050b.jpg',
        }

        '''
        # hash user inputted image
        fields = [
        ]
        params ={
            'filename': '/Users/justinshaw/Documents/code/herokuApps/fbapp01/static/image1.jpeg', # /image1.jpeg,
            'parent_id': ad_details['adaccount_id'],
        }
        image = AdImage(ad_details['adaccount_id']).api_create(
            parent_id=ad_details['adaccount_id'],
            params=params,
        )
        print(image)
        hash = image['hash']
        '''
        # instead of hashing user inputted photo, hardcode a photo from test account
        hash = '3c57436a2eb2c2e887241086c8aa226f'


        # add more necessary values to dict that require manipulation
        property_details.update ({
            'headline': '2XX,XXX!',
            'message': "\N{FIRE}" + ' Hot ' + property_details['query_city'] + ' area listing ' + "\N{FIRE}!!" + '\n\nBEDS: ' + property_details['beds'] + '\nBATHS: ' + property_details['baths'] + '\nSQ FT: ' + property_details['sqft'] + '\n\nTo see the price, location, and more pictures, tap "Learn More"',
            "image_hash": "3c57436a2eb2c2e887241086c8aa226f", # returned from above function
        })


        #test1 = db.execute("INSERT INTO ads (query_address, query_city, price, beds, baths, sqft, scraped_address, scraped_image) VALUES (:query_address, :query_city, :price, :beds, :baths, :sqft, :scraped_address, :scraped_image)",
                    #query_address=property_details['query_address'], query_city=property_details['query_city'], price=property_details['price'], beds=property_details['beds'], baths=property_details['baths'], sqft=property_details['sqft'], scraped_address=property_details['scraped_address'], scraped_image=property_details['scraped_image'])
        #test2 = db.execute("INSERT INTO ads (query_address, query_city, price, beds, baths, sqft, scraped_address, scraped_image, message, headline, image_hash) VALUES (:query_address, :query_city, :price, :beds, :baths, :sqft, :scraped_address, :scraped_image, :message, :headline, :image_hash)",
                    #query_address=property_details['query_address'], query_city=property_details['query_city'], price=property_details['price'], beds=property_details['beds'], baths=property_details['baths'], sqft=property_details['sqft'], scraped_address=property_details['scraped_address'], scraped_image=property_details['scraped_image'], message=property_details['message'], headline=property_details['headline'], image_hash=property_details['image_hash'])
        test3 = db.execute("INSERT INTO ads (query_address, query_city, price, beds, baths, sqft, scraped_address, scraped_image, message, headline, image_hash, page_id, adaccount_id, adaccount_name, lead_gen_form_id, privacy_policy_url, property_url) VALUES (:query_address, :query_city, :price, :beds, :baths, :sqft, :scraped_address, :scraped_image, :message, :headline, :image_hash, :page_id, :adaccount_id, :adaccount_name, :lead_gen_form_id, :privacy_policy_url, :property_url)",
                    query_address=property_details['query_address'], query_city=property_details['query_city'], price=property_details['price'], beds=property_details['beds'], baths=property_details['baths'], sqft=property_details['sqft'], scraped_address=property_details['scraped_address'], scraped_image=property_details['scraped_image'], message=property_details['message'], headline=property_details['headline'], image_hash=property_details['image_hash'], page_id=ad_details['page_id'], adaccount_id=ad_details['adaccount_id'], adaccount_name=ad_details['adaccount_name'], lead_gen_form_id=ad_details['lead_gen_form_id'], privacy_policy_url=ad_details['privacy_policy_url'], property_url=ad_details['property_url'])

    # if user is updating preview, just update the database
    if request.form.get("budget"): # update the database
        print("running if budget")
        print("updating database!")
        # update database
        #test3 = db.execute("INSERT INTO ads (budget, duration, adaccount_id, headline, message, property_url, privacy_policy_url) VALUES (:budget, :duration, :adaccount_id, :headline, :message, :property_url, :privacy_policy_url)",
                    #budget = request.form.get("budget"), duration= request.form.get("duration"), adaccount_id = request.form.get("adaccount_id"), headline = request.form.get("headline"), message = request.form.get("adtext"), property_url = request.form.get("property_url"), privacy_policy_url = request.form.get("privacy_policy_url"))
        #test3 = db.execute("INSERT INTO ads (query_address, query_city, price, beds, baths, sqft, scraped_address, scraped_image, message, headline, image_hash, page_id, adaccount_id, adaccount_name, lead_gen_form_id, privacy_policy_url, property_url) VALUES (:query_address, :query_city, :price, :beds, :baths, :sqft, :scraped_address, :scraped_image, :message, :headline, :image_hash, :page_id, :adaccount_id, :adaccount_name, :lead_gen_form_id, :privacy_policy_url, :property_url)",
                    #query_address=property_details['query_address'], query_city=property_details['query_city'], price=property_details['price'], beds=property_details['beds'], baths=property_details['baths'], sqft=property_details['sqft'], scraped_address=property_details['scraped_address'], scraped_image=property_details['scraped_image'], message=property_details['message'], headline=property_details['headline'], image_hash=property_details['image_hash'], page_id=ad_details['page_id'], adaccount_id=ad_details['adaccount_id'], adaccount_name=ad_details['adaccount_name'], lead_gen_form_id=ad_details['lead_gen_form_id'], privacy_policy_url=ad_details['privacy_policy_url'], property_url=ad_details['property_url'])
        ad_details = {
            'budget': request.form.get('budget'),
            'duration': request.form.get('duration'),
            'adaccount_id': request.form.get('adaccount_id'),
            'message': request.form.get('message'),
            'headline': request.form.get('headline'),
            'property_url': request.form.get('property_url'),
            'privacy_policy_url': request.form.get('privacy_policy_url'),
        }
        print(ad_details)

        id = request.form.get('id') # get id of column in ads tables
        print(id)

        ad = db.execute("SELECT * FROM ads WHERE id= :id", id=id)
        db.execute("UPDATE ads SET budget = :budget, duration = :duration, adaccount_id = :adaccount_id, message = :message, headline = :headline, privacy_policy_url = :privacy_policy_url, property_url = :property_url WHERE id = :id", budget = ad_details['budget'], duration = ad_details['duration'], adaccount_id = ad_details['adaccount_id'], message = ad_details['message'], headline = ad_details['headline'], privacy_policy_url = ad_details['privacy_policy_url'], property_url =
                    ad_details['property_url'], id = id)
        print(ad)
        test3 = id
        print(test3)

    # generate preview - call variables from database
    ad = db.execute("SELECT * FROM ads WHERE id= :id", id=test3) # retrieve user info from database to later store in session
    ad = ad[0]
    print(ad['message'])


    # generate leads ad w/ status draft
    print("running preview")
    fields = [
    ]
    params = {  #  these fields can be found in under the page reference: https://developers.facebook.com/docs/graph-api/reference/page/
      'name': ad['message'],
      'follow_up_action_url': ad['property_url'],
      'question_page_custom_headline': 'question page title',
      'questions': [
          {
            "key": "budget?",
            "label": "Budget?",
            "options": [
              {
                "key": "under_300k",
                "value": "under 300k"
              },
              {
                "key": "300k-600k",
                "value": "300k-600k"
              },
              {
                "key": "over_700k",
                "value": "over 700k"
              }
            ],
            "type": "CUSTOM"
          },
          {
            "key": "when_do_you_want_keys_to_your_home?",
            "label": "When Do You Want Keys To Your Home?",
            "options": [
              {
                "key": "within_3_months",
                "value": "Within 3 months"
              },
              {
                "key": "3-6months",
                "value": "3-6months"
              },
              {
                "key": "more_than_6_months",
                "value": "More than 6 Months"
              }
            ],
            "type": "CUSTOM"
          },
          {
            "key": "email",
            "type": "EMAIL",
          },
          {
            "key": "full_name",
            "type": "FULL_NAME",
          }
          ],
      'privacy_policy': {'url': ad['privacy_policy_url'], 'link_text': 'privacy'}, # https://developers.facebook.com/docs/graph-api/reference/page/

    "thank_you_page": {
      "title": "Great! You're All Set.",
      "body": "One of our agents will be in touch to help you customize your home search! Tap below to view the location, price, and more pictures!",
      "button_text": "SEE THE INSIDE!!",
      "enable_messenger": False,
      "button_type": "VIEW_WEBSITE",
      "website_url": ad['property_url'],
      },
     # "leadgen_tos_accepted": True
    }

    params['name'] = params['name'] + str(randint(100, 999)) #add one to the form name so it's always unique

    page_access_token = os.getenv("TEST_PAGE_ACCESS_TOKEN")
    print('@@@@@@@@@@page_access_token@@@@@@@@@@@@')
    print(page_access_token)
    FacebookAdsApi.init(access_token=page_access_token)

    lead_gen_form = Page(ad['page_id']).create_lead_gen_form( # must use page_access_token
      fields=fields,
      params=params,
    )

    # update lead_form_id in database
    db.execute("INSERT INTO ads (lead_gen_form_id) VALUES (:lead_gen_form_id)",
               lead_gen_form_id=lead_gen_form['id'])
    # generate ad preview
    # pass values to HTML

    # METHOD 2: generate an ad preview from a non-existing ad: https://developers.facebook.com/docs/marketing-api/generatepreview/v3.2
    # two steps: (1) create an object_story_spec and (2) use the gen_generate_previews function from the user's ad account node
    #print("method 2:")
    params1 = {
        'object_story_spec': {
            'page_id': ad['page_id'],
            'link_data': {
                'message': ad['message'],
                'link': 'http://fb.me/',
                'image_hash': ad['image_hash'],
                'name': ad['headline'],
                #'caption':'WWW.ITUNES.COM',
                #'description':'The link description',
                #'title': adheadline,
                'call_to_action': {
                    'type':'LEARN_MORE',
                    'value': {
                        'link':'http://fb.me/',
                        'lead_gen_form_id': lead_gen_form['id']
                    }
                }
            }
        },
    }

    params = {
        'creative': params1, # how to use a creative spec? https://developers.facebook.com/docs/marketing-api/reference/ad-creative
        'ad_format': 'MOBILE_FEED_STANDARD',
        }
    adpreview = AdAccount(ad['adaccount_id']).get_generate_previews(params=params)


    # now that we have the ad preview, get <iframe> to display on html page
    adpreview = adpreview[0]['body']
    soup = BeautifulSoup(adpreview, 'html5lib')
    iframe2 = soup.find_all('iframe')[0]['src']

    # try to get a preview
    fields = [
    ]
    params = {
        'creative': 'creative', # how to use a creative spec? https://developers.facebook.com/docs/marketing-api/reference/ad-creative
        'ad_format': 'MOBILE_FEED_STANDARD',
        }

    return render_template("showpreview.html", iframe2=iframe2, testdict=ad)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) # app.run(ssl_context='adhoc', host='0.0.0.0', port=port)
