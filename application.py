
# heroku URL: https://fbapp0111.herokuapp.com/


# access environment variables via dotenv library: https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path = Path('.gitignore') / '.env'
load_dotenv(dotenv_path=env_path)

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

from helpers import apology, login_required, lookup
import psycopg2

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



# log in info

app_secret = os.getenv("APP_SECRET")  # os.environ["APP_SECRET"]
app_id = '342529826361699' #test app #main app: '2446850972202703'  #!!be sure to change web_id in JS SDK in layout.html
# id = 'act_804097463107225' # Justin Shaw ad account is 'act_804097463107225', test ad account is 'act_255618438702332'
# page_id:'1775351279446344' # Shaw Marketing page id

# FacebookAdsApi.init(account_id=id, access_token=access_token)
SECRET_KEY = app_secret
FB_APP_ID = app_id
FB_APP_SECRET = app_secret



# https://stackoverflow.com/questions/45133831/heroku-cant-launch-python-flask-app-attributeerror-function-object-has-no
urllib.parse.uses_netloc.append("postgres")
# urllib.uses_netloc.parse.append("postgres")
url = urllib.parse.urlparse(os.getenv("DATABASE_URL"))


'''
conn = psycopg2.connect(
 database=url.path[1:],
 user=url.username,
 password=url.password,
 host=url.hostname,
 port=url.port
)

# Open a cursor to perform database operations
# http://www.psycopg.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries
cur = conn.cursor()
'''

'''
# Configure CS50 Library to use SQLite database
db = SQL(os.getenv("DATABASE_URL"))
# db = SQL("sqlite:///recipes.db")
'''
db = SQL(os.environ["DATABASE_URL"]) # os.environ["APP_SECRET"]

# Configure application
app = Flask(__name__)
# sslify = SSLify(app)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

'''
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
'''
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/deleteleads", methods=["GET", "POST"])
def deleteleads():
    db.execute("DELETE FROM leads WHERE page_id='1775351279446344'")
    return redirect("/")

@app.route("/preview", methods=["GET", "POST"])
def preview():

    # hardcode so don't have to login
    user_access_token = os.getenv("TEST_USER_ACCESS_TOKEN")
    page_access_token = os.getenv("TEST_PAGE_ACCESS_TOKEN")
    FacebookAdsApi.init(access_token=page_access_token)

    if request.method =="GET":

        # you can set key as config
        places_api_key = os.getenv("GOOGLEMAPS_PLACES_API_KEY")
        app.config['places_api_key'] = places_api_key
        return render_template("enterurl.html", places_api_key=places_api_key)
    else:
        print("running POST /preview")


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

@app.route("/generatepreview", methods=["GET", "POST"])
def generatepreview(): #takes in url and outputs html page
    if request.method == "GET":
        return render_template("enterurl.html")
    else:
        property_url = request.form.get("property_url")

        # make sure form filled out
        if not property_url:
            flash('Must provide a URL', 'error')
            return redirect("/generatepreview")

        # get variables from scraper() fxn
        print(storevalues(scraper(property_url)))

        # make form

        # make campaign

        # make ad Set

        # make creative

        # make ad

        # generate ad preview

        # pass ad preview iframe to "/FXNWhereSeePreviewANDCanEdit6Variables"
        return render_template("terms.html")
def storevalues(property_details):
    save = db.execute("INSERT INTO ads (page_id, price, bed, bath, sqft, address) VALUES (:page_id, :price, :bed, :bath, :sqft, :address)",
               page_id='1775351279446344', price=property_details['price'], bed=property_details['bed'], bath=property_details['bath'], sqft=property_details['sqft'], address=property_details['address'])
    print("ad stored in the database")
    print(save)
    return('', 203)


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("running /webhook on application.py")
    if request.method == "POST":

        data = request.get_json()
        # print(data)

        if data["object"] == "page": # make sure incoming ping is from a page

            for entry in data["entry"]: # account for more than one lead at a time
                page_id = entry['id']

                for lead_event in entry["changes"]:

                    print( 'page_id: ' + page_id )
                    leadform = lead_event['value']['form_id']
                    print('leadform: ' + leadform)
                    lead_id = lead_event['value']['leadgen_id']
                    print('lead_id: ' + lead_id)

                    # Method 2: make a GET request for lead info using Facebook-SDK library
                    '''
                    graph = GraphAPI('356ethw346w3rasg3y') # i have the access token stored in variable "graph"
                    lead = graph.get_object(lead_id) # i have the profile into stored in "profile"
                    print(lead)
                    '''
                    # Method 1: make a GET request for lead info using the official Python Business SDK
                    #user_access_token = os.getenv("TEST_USER_ACCESS_TOKEN")
                    page_access_token = os.getenv("TEST_PAGE_ACCESS_TOKEN")
                    #FacebookAdsApi.init(access_token=page_access_token)
                    FacebookAdsApi.init(access_token=page_access_token)
                    fields = [
                    ]
                    params = {
                    }
                    data = Lead(lead_id).api_get(
                      fields=fields,
                      params=params,
                    )

                    # for each datafield returned by the leadgen_id, save it to a variable
                    for field_data in data["field_data"]:
                        if field_data["name"]=='email':
                            email = field_data["values"][0]

                        elif field_data["name"] == 'full_name':
                            full_name = field_data["values"][0]
                            print(field_data["values"])

                    # for each lead, store lead in SQL database
                    db.execute("INSERT INTO leads (page_id, full_name, email) VALUES (:page_id, :full_name, :email)",
                               page_id=page_id, full_name=full_name, email=email)

                    # for each lead, send an SMS to the respective user
                    user = db.execute("SELECT * FROM users WHERE page_id = :page_id", page_id=page_id) # retrieve user info from database to later store in session
                    print(user[0])
        return redirect('/')

    else:
        if request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == os.getenv("VERIFY_TOKEN"):
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200
        return "hello world", 200

@app.route("/terms", methods=["GET", "POST"])
def terms():
    print("##### terms/logout ######")
    session.pop("user", None)
    return render_template("terms.html", user=g.user)

@app.before_request
def get_current_user():
    print("@@running get_current_user@@")

    if session.get("user"):
        g.user = session.get("user")
        print("@@found a g.user so I'm ending get_current_user@@")
        return
    # Attempt to get the short term access token for the current user.


    result = get_user_from_cookie(
        cookies=request.cookies, app_id=FB_APP_ID, app_secret=FB_APP_SECRET
    )
    print("result:")
    print(result)

    if result: # only runs if facebook login returns a result (i.e. user is logged in)

        # Check to see if this user is already in our database.
        print('result["uid"]')
        print(result["uid"])
        user = db.execute("SELECT * FROM users WHERE user_id = :uid", uid=result["uid"]) # returns an object: https://docs.cs50.net/problems/finance/finance.html#hints
        #print(User.query.filter(User.user_id == result["uid"]).first())
        #user = User.query.filter(User.user_id == result["uid"]).first() # search "user" database to see if it has the user_id
        rows = user
        print(rows)


        #if not user:
        if not user:
            print("access token:")
            print(result["access_token"])

            graph = GraphAPI(result["access_token"]) # i have the access token stored in variable "graph"
            profile = graph.get_object("me") # i have the profile into stored in "profile"
            if "link" not in profile:
                profile["link"] = ""
            print("graph:")
            print(graph)
            print("profile:")
            print(profile)
            print("Access Token:")
            print(result["access_token"])
            print("results:")
            print(result)

            # Create the user and insert it into the database
            user = db.execute("INSERT INTO users (user_id, access_token, profile_url) VALUES (:uid, :access, :profile)",
                               uid=str(profile["id"]), access=result["access_token"], profile=profile["link"]) # returns unique "id" of the user
            rows = db.execute("SELECT * FROM users WHERE id = :id", id=user) # retrieve user info from database to later store in session
            print(rows[0]["user_id"])

        elif user[0]["access_token"] != result["access_token"]:
            # If an existing user, update the access token
            print("################ access tokens not equal - see line 142 of code")
            user[0]["access_token"] = result["access_token"]

        # Add the user to the current session
        print(rows)
        session["user"] = dict(
            #name=user.name, # get name value from heroku database
            profile_url=rows[0]["profile_url"],
            user_id=rows[0]["user_id"],
            access_token=rows[0]["access_token"],
        )

    # set the user as a global g.user
    g.user = session.get("user", None)
    if g.user:
        print(g.user) # the following don't work - print(g.user["access_token"]) || print(g.user.access_token)
    if not g.user:
        print("@@no g.user@@")
    return

@app.route("/", methods=["GET", "POST"])
#@login_required
def crm():
    if request.method == "POST":
        pass
    else:
        # rows = db.execute("SELECT * FROM leads WHERE id IN (SELECT region FROM top_regions)= :username", username=username)
        # rows = db.execute("SELECT * FROM leads WHERE user = :username", username=userId)
        '''
        # add a new lead everytime I load the page
        db.execute("INSERT INTO leads (page_id, full_name, email) VALUES (:page_id, :full_name, :email)",
                                        page_id='1775351279446344', full_name='Justin Shaw', email='test'+ str(randint(100, 999)) + '@email.com')
        '''
        rows = db.execute("SELECT * FROM leads WHERE page_id = '1775351279446344'")
        count = len(rows)
        return render_template("index.html", count=count, rows=rows)

@app.route("/tools", methods=["GET", "POST"])
#@login_required
def tools():
    if request.method == "POST":
        pass
    else:
        print("in /tools")
        return render_template("tools.html")


@app.route("/leadads", methods=["GET", "POST"])
#@login_required
def leadads():
    if request.method == "POST":

        if not request.form.get("adaccount"):
            flash('Must select an Ad Account', 'error')
            return redirect("/leadads")
        elif not request.form.get("adtext"):
            flash('Must provide Ad Text', 'error')
            return redirect("/leadads")
        elif not request.form.get("adimage"):
            flash('Must provide Ad Image', 'error')
            return redirect("/leadads")
        elif not request.form.get("adheadline"):
            flash('Must provide Ad Headline', 'error')
            return redirect("/leadads")
        else:
            session['adaccount'] = request.form.get("adaccount") #save user adaccount in Session
            adaccount = session['adaccount']
            session['adtext'] = request.form.get("adtext") # save user adtext in Session
            adtext = session['adtext']
            session['adimage'] = request.form.get("adimage") # save user adimage in Session
            adimage = session['adimage']
            session['adheadline'] = request.form.get("adheadline") # save user adheadline in Session
            adheadline = session['adheadline']
            print(adimage)
            print(adheadline)

            # hash user inputted image
            fields = [
            ]
            params ={
                'filename': 'static/demoad1.png',
                'parent_id': 'act_123',
            }
            image = AdImage(adaccount).api_create(
                parent_id=adaccount,
                params=params,
            )
            print(image)
            hash = image['hash']

            # set the API for future API calls within this function
            #FacebookAdsApi.init(access_token=g.user['access_token']) # requires user access token

            #let's try to create a lead form
            fields = [
            ]
            params = {  #  these fields can be found in under the page reference: https://developers.facebook.com/docs/graph-api/reference/page/
              'name': adtext,
              'follow_up_action_url': 'https://fbapp0111.herokuapp.com/',
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
              #'privacy_policy_url': "https://fbapp0111.herokuapp.com/terms",
              #'privacy_policy': 'Object',
              'privacy_policy': {'url': "https://fbapp0111.herokuapp.com/terms", 'link_text': 'privacy'}, # https://developers.facebook.com/docs/graph-api/reference/page/
              #'legal_content_id': 'string',

            "thank_you_page": {
              "title": "Great! You're All Set.",
              "body": "Feel free to access the property info below now.",
              "button_text": "View Property Details",
              "enable_messenger": False,
              "button_type": "VIEW_WEBSITE",
              "website_url": "https://fbapp0111.herokuapp.com/",
              },
             # "leadgen_tos_accepted": True
            }
            FacebookAdsApi.init(access_token=session['page_access_token'])
            lead_gen_form = (Page(session['page_id']).create_lead_gen_form( # ABC realty  page_id: 218711598949970 shaw marketing page_id: #1775351279446344
              fields=fields,
              params=params,
            ))

            # create campaign
            fields = [
            ]
            params ={
                'name': adtext,
                'objective': 'LEAD_GENERATION',
                'status': "PAUSED",
                'buying_type': "AUCTION",
            }
            newcampaign = AdAccount(adaccount).create_campaign(
                fields=fields,
                params=params,
            )
            session['campid'] = newcampaign["id"]  # save campaign id in session

            # create adset
            fields = [
            ]
            params = {
              'name': adtext,
              'optimization_goal': 'LEAD_GENERATION', #or LINK_CLICKS
              'billing_event': 'IMPRESSIONS',
              'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
              'daily_budget': '100',
              'campaign_id': session['campid'],
              'targeting': {
                "age_max": 65,
                "age_min": 18,
                "geo_locations": {
                  "countries": [
                    "US"
                  ],
                  "location_types": [
                    "home",
                    "recent"
                  ]
                },
                "publisher_platforms": [
                  "facebook"
                ],
                "facebook_positions": [
                  "feed"
                ],
                "device_platforms": [
                  "mobile"#,
                  #"desktop"
                ]
              },
              'status': 'PAUSED',
              'promoted_object': {'page_id': session['page_id']}, # get from session storage
            }
            newadset = AdAccount(adaccount).create_ad_set(
              fields=fields,
              params=params,
            )
            session['adsetid'] = newadset["id"] # save ad set id in session

            #generate ad AdPreview (0)lead form (1) ad creative (2) preview
            # create ad creative (afterwards we'll create the actual ad) # ad creative: 23843836492140536
            fields = [
            ]
            params = {
                'object_story_spec': {
                    'page_id':session['page_id'],
                    'link_data': {
                        'message': adtext,
                        'link': 'http://fb.me/',
                        'image_hash': hash,
                        'name': adheadline,
                        #'caption':'WWW.ITUNES.COM',
                        #'description':'The link description',
                        #'title': adheadline,
                        'call_to_action': {
                            'type':'SIGN_UP',
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
            newcreative = AdAccount(adaccount).create_ad_creative( # requires user access token
              fields=fields,
              params=params,
            )


            # generate a preview
            account = AdAccount(adaccount)

            '''
            # Method 1: generate a preview from an unpublished ad_creative: https://developers.facebook.com/docs/marketing-api/generatepreview/v3.2
            params = {
              'ad_format': 'MOBILE_FEED_STANDARD',
              #'creative': newcreative.export_data(),
              'creative': <creative>
            adpreview = account.get_generate_previews(params=params)
            session['adpreview'] = adpreview[0]['body']
            '''

            #Method 2: generate a preview from a published create_ad_creative
            fields = [
            ]
            params = {
              'ad_format': 'MOBILE_FEED_STANDARD',
            }
            adpreview = AdCreative(newcreative["id"]).get_previews(  # uses a user access token (not a page access token)
              fields=fields,
              params=params,
            )
            session['adpreview'] = adpreview[0]['body']

            # now that we have ad creative, let's create the ad
            fields = [
            ]
            params = {
              'name': 'My Ad',
              'adset_id': newadset["id"],
              'creative': {'creative_id': newcreative["id"]},
              'status': 'PAUSED',
            }
            newad = AdAccount(adaccount).create_ad(
              fields=fields,
              params=params,
            )

            # save the ad account
            session['adaccount'] = adaccount

            # get previews ready
            adpreview = session['adpreview'] # retrieved from /leadads
            soup = BeautifulSoup(adpreview, 'html5lib')
            iframe = soup.find_all('iframe')[0]['src']

            # get variables to render AdAccounts
            # adaccounts = session['adaccounts']
            #access_token = g.user['access_token']
            #FacebookAdsApi.init(access_token=access_token)
            user_id = g.user['user_id']
            fields = [
                'name',
            ]
            params = {
            }
            adaccounts = (User(user_id).get_ad_accounts(  # assuming id is the user_id
              fields=fields,
              params=params,
            ))
            count = len(adaccounts)

            return render_template("leadadspreview.html", iframe=iframe, adaccounts=adaccounts, count=count)

    else:
        print("@@@@@@ g.user @@@@@")
        print(g.user)
        if not session.get("user"): # since user is not logged in, prompt them to login
            return render_template("fblogin.html", app_id=FB_APP_ID)
        elif session.get("user"): # user is logged in
        #try:
            user_id = g.user['user_id']
            access_token = g.user['access_token']
            FacebookAdsApi.init(access_token=access_token)
            graph = facebook.GraphAPI(access_token=access_token)
            pages_data = graph.get_object("/me/accounts")

            page_access_token = pages_data['data'][0]['access_token']  # https://medium.com/@DrGabrielA81/python-how-making-facebook-api-calls-using-facebook-sdk-ea18bec973c8
            page_id = pages_data['data'][0]['id']  # page_id
            session['page_access_token'] = page_access_token
            session['page_id'] = page_id

            #FacebookAdsApi.init(access_token=page_access_token)


            #id = adaccounts[0]["id"]
            #print("id")
            #print(id)
            print(adaccounts)
            count = len(adaccounts)
            session['count'] = count
            #session['count'] = adaccounts
            print("rendering template ads.html")
            return render_template("leadads.html", user=g.user, adaccounts=adaccounts, count=count)

@app.route("/publishleadads", methods=['GET','POST'])
def publishleadads():
    if request.method =="POST":
        print('Make it Live!')

@app.route("/leadads_step2", methods=["GET", "POST"])
def leadads_step2():
    if request.method == "GET":
        return redirect("/leadads")
    else:
        if not request.form.get("adaccount"):
            flash('Must select an ad account', 'error')
            return redirect("/leadads")
        else:
            session['adaccount'] = request.form.get("adaccount") # save ad account in Session
            print('adaccount:' + session['adaccount'])
            return render_template("leadads_step2.html") # send user to next step -- step 2


@app.route("/leadads_step3", methods=["GET", "POST"])
def leadads_step3():
    if request.method == "GET":
        return render_template("leadads_step2.html")
    else:
            return render_template("leadads_step3.html") # send user to next step -- step 2


@app.route("/ads", methods=["GET", "POST"])
#@login_required
def ads():
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

            '''
            # create ad set - v2.0 - https://github.com/facebook/facebook-python-business-sdk/blob/master/examples/AdAccountAdSetsPostReach.py
            fields = [
            ]
            params = { # https://developers.facebook.com/docs/marketing-api/reference/ad-campaign
              'name': adsetname,
              'optimization_goal': 'REPLIES', #or LINK_CLICKS
              'billing_event': 'IMPRESSIONS',
              'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
              'daily_budget': '100',
              'campaign_id': newcampaign["id"],
              # platform targeting : https://developers.facebook.com/docs/marketing-api/targeting-specs#placement
              'targeting': {
                "age_max": 65,
                "age_min": 18,
                "geo_locations": {
                  "countries": [
                    "US"
                  ],
                  "location_types": [
                    "home",
                    "recent"
                  ]
                },
                "publisher_platforms": [
                  "facebook"
                ],
                "facebook_positions": [
                  "feed"
                ],
                "device_platforms": [
                  "mobile",
                  "desktop"
                ]
              }, # use graph API "/23843808299360536?fields=targeting", where # is ad id
              'status': 'PAUSED',
              #'promoted_object': {'page_id':'1775351279446344'}, # page_id id not available
            }
            print("made it past the paramater")
            newadset = AdAccount(adaccount).create_ad_set(
              fields=fields,
              params=params,
            )
            print("new ad set:")
            print(newadset["id"])


            # create ad
            fields = [
            ]
            params = {
              'name': 'My Ad',
              'adset_id': newadset["id"],
              #'creative': {'creative_id': '23843808299800536'}, # to get the creative associated with an exiting ad use: "23843808299510536/adcreatives", where first number is ad id, which can be found in ad manager stats
              'status': 'PAUSED',
            }
            print (AdAccount(adaccount).create_ad(
              fields=fields,
              params=params,
            ))

        #except: # the try failed, and I think it's b/c of the id
            #print("the previous function failed - here's the id")
            #print(id)
            #return redirect("/ads")
            '''
            session['adaccount'] = adaccount
            print(session['adaccount'])
            return redirect("/adresults")
    else:
        print("@@@@@@ g.user @@@@@")
        print(g.user)
        if not session.get("user"): # since user is not logged in, prompt them to login
            return render_template("fblogin.html", app_id=FB_APP_ID)
        elif session.get("user"): # user is logged in
        #try:
            user_id = g.user['user_id']
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(user_id)
            access_token = g.user['access_token']
            print(access_token)
            FacebookAdsApi.init(access_token=access_token)
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

        # Remember which user has logged in
        global userId
        userId = rows[0]["id"]
        session["user_id"] = userId
        print(userId)

        # need to access the first row of the array rows, row[0] and then go to the index cash, ["cash"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


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

        # Remember which user has logged in
        global userId
        userId = rows[0]["id"]
        session["user_id"] = userId

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


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
 port = int(os.environ.get('PORT', 5000))  #getenv  # port = int(os.environ.get('PORT', 5000))
 app.run(host='0.0.0.0', port=port)
 # app.run(host='0.0.0.0', port=8000)
 #app.config['SESSION_TYPE'] = 'filesystem' # https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension
 #Session(app)
 # The session is unavailable because no secret key was set. Set the secret_ key on the application to something unique and secret.
