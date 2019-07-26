# generate_preview
import os

from flask import g, Flask, flash, jsonify, redirect, render_template, request, session

from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.page import Page

from facebook_business.adobjects.leadgenformpreviewdetails import LeadGenFormPreviewDetails

from bs4 import BeautifulSoup

from random import randint

from scraper import scraper

#import emoji #https://pypi.org/project/emoji/



user_access_token = os.environ["TEST_USER_ACCESS_TOKEN"]
page_access_token = os.environ["TEST_PAGE_ACCESS_TOKEN"]
app_secret = os.environ["TEST_APP_SECRET"]
app_id = '342529826361699'
id = '23843836492140536'
FacebookAdsApi.init(access_token=page_access_token)

app = Flask(__name__) # define app


@app.route("/preview", methods=["GET", "POST"])
def generatepreview():
    if request.method =="GET":
        return render_template("enterurl.html")
    else:
        if not request.form.get("budget"): # if user just typed in URL, run scraper
            global testdict
            print(request.form.get('query_address'))
            testdict = scraper(request.form.get('query_address')) # call the scraper function with the query_address
            # add more necessary values to dict that require manipulation
            testdict.update ({
                'headline': '4XX,XXX!',
                'message': "\N{FIRE}" + ' Hot ' + testdict['query_city'] + ' area listing!! ' + "\N{FIRE}" + '\n\nBEDS: ' + testdict['beds'] + '\nBATHS: ' + testdict['baths'] + '\nSQ FT: ' + testdict['sqft'] + '\n\nTo see the price, location, and more pictures, tap "Learn More"',
                "image_hash": "34f6008a0cd588440c37e5233c1b3042", # returned from above function
            })


            # add last necessary values to dict -- added to database table as default
            testdict.update ({
              "page_id": "1775351279446344",
              "adaccount_id": 'act_804097463107225',
              'adaccount_name': 'Justin Shaw',
                "lead_gen_form_id": "1196489520508599",
                "privacy_policy_url": "fbapp0111.herokuapp.com/terms",
                "property_url": "soldoncharleston.com/property/19004415",
                "budget": 5,
                "duration": 3
            })

            '''
            testdict =	{
              "page_id": "1775351279446344",
              "adaccount_id": 'act_804097463107225',
              'adaccount_name': 'Justin Shaw',
              "message": "\N{FIRE}" + ' Hot [CITY] area listing!! ' + "\N{FIRE}" + '\n\nBEDS: [BEDS]\nBATHS: [BATHS]\nSQ FT: [SQFT]\n\nTo see the price, location, and more pictures, tap "Learn More"',
              "image_hash": "34f6008a0cd588440c37e5233c1b3042",
              "headline": "4XX,XXX!",
              "lead_gen_form_id": "1196489520508599",
              "privacy_policy_url": "fbapp0111.herokuapp.com/terms",
              "property_url": "soldoncharleston.com/property/19004415",
              "scraped_url": 'https://www.soldoncharleston.com/property/19004415',
              "budget": 5,
              "duration": 3,
              'city': "CHARLESTON",
              'beds': 3,
              'baths': 3,
              'sqft': 2035,
              #'price': '400000',
            } # demo database
            '''

        if request.form.get("budget"): # update the database
            print("updating database!")
            # update database
            testdict['budget'] = request.form.get("budget")
            testdict['duration'] = request.form.get("duration")
            testdict['adaccount_id'] = request.form.get("adaccount_id")
            testdict['headline'] = request.form.get("headline")
            testdict['message'] = request.form.get("adtext")
            testdict['property_url'] = request.form.get("property_url")
            testdict['privacy_policy_url'] = request.form.get("privacy_policy_url")
            #print(testdict)

        # generate leads ad w/ status draft
        fields = [
        ]
        params = {  #  these fields can be found in under the page reference: https://developers.facebook.com/docs/graph-api/reference/page/
          'name': testdict['message'],
          'follow_up_action_url': testdict['property_url'],
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
          'privacy_policy': {'url': testdict['privacy_policy_url'], 'link_text': 'privacy'}, # https://developers.facebook.com/docs/graph-api/reference/page/

        "thank_you_page": {
          "title": "Great! You're All Set.",
          "body": "One of our agents will be in touch to help you customize your home search! Tap below to view the location, price, and more pictures!",
          "button_text": "SEE THE INSIDE!!",
          "enable_messenger": False,
          "button_type": "VIEW_WEBSITE",
          "website_url": testdict['property_url'],
          },
         # "leadgen_tos_accepted": True
        }

        params['name'] = params['name'] + str(randint(100, 999)) #add one to the form name so it's always unique

        lead_gen_form = Page(testdict['page_id']).create_lead_gen_form( # must use page_access_token
          fields=fields,
          params=params,
        )
        testdict["lead_gen_form_id"] = lead_gen_form['id'] # add lead_form_id to #thisdict

        # generate ad preview
        # pass values to HTML


        # METHOD 1: generate an ad preview from an existing ad, given a page_access_token and creative_id
        #print("method 1:")
        fields = [
        ]
        params = {
          'ad_format': 'MOBILE_FEED_STANDARD',
        }
        newcreative = AdCreative(id).get_previews(
          fields=fields,
          params=params,
        )

        # METHOD 2: generate an ad preview from a non-existing ad: https://developers.facebook.com/docs/marketing-api/generatepreview/v3.2
        # two steps: (1) create an object_story_spec and (2) use the gen_generate_previews function from the user's ad account node
        #print("method 2:")
        params1 = {
            'object_story_spec': {
                'page_id': testdict['page_id'],
                'link_data': {
                    'message': testdict['message'],
                    'link': 'http://fb.me/',
                    'image_hash': testdict['image_hash'],
                    'name': testdict['headline'],
                    #'caption':'WWW.ITUNES.COM',
                    #'description':'The link description',
                    #'title': adheadline,
                    'call_to_action': {
                        'type':'SIGN_UP',
                        'value': {
                            'link':'http://fb.me/',
                            'lead_gen_form_id': testdict['lead_gen_form_id']
                        }
                    }
                }
            },
        }

        params = {
            'creative': params1, # how to use a creative spec? https://developers.facebook.com/docs/marketing-api/reference/ad-creative
            'ad_format': 'MOBILE_FEED_STANDARD',
            }
        adpreview = AdAccount(testdict['adaccount_id']).get_generate_previews(params=params)


        # now that we have the ad preview, get <iframe> to display on html page
        newcreative = newcreative[0]['body'] # get the body of the api return statement
        soup = BeautifulSoup(newcreative, 'html5lib') # make the body in a format BeautfulSoup can understand
        iframe1 = soup.find_all('iframe')[0]['src'] # get the iframe out of the BeautifulSoup

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

        return render_template("showpreview.html", iframe1=iframe1, iframe2=iframe2, testdict=testdict)

@app.route("/ads", methods=["GET", "POST"])
def ads():
    # get ad info from DB, since it was stored after person previewed the ad
    if request.method =="POST":

        # create a lead form
        fields = [
        ]
        params = {  #  these fields can be found in under the page reference: https://developers.facebook.com/docs/graph-api/reference/page/
          'name': 'Lead Ad: ' + testdict['message'],
          'follow_up_action_url': testdict['property_url'],
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
          'privacy_policy': {'url': testdict['privacy_policy_url'], 'link_text': 'privacy'}, # https://developers.facebook.com/docs/graph-api/reference/page/
          #'legal_content_id': 'string',

        "thank_you_page": {
          "title": "Great! You're All Set.",
          "body": "Feel free to access the property info below now.",
          "button_text": "View Property Details",
          "enable_messenger": False,
          "button_type": "VIEW_WEBSITE",
          "website_url": testdict['property_url'],
          },
         # "leadgen_tos_accepted": True
        }
        lead_gen_form = (Page(testdict['page_id']).create_lead_gen_form( # ABC realty  page_id: 218711598949970 shaw marketing page_id: #1775351279446344
          fields=fields,
          params=params,
        ))

        # create campaign
        fields = [
        ]
        params ={
            'name': 'Lead Ad Campaign',
            'objective': 'LEAD_GENERATION',
            'status': "PAUSED",
            'buying_type': "AUCTION",
        }
        newcampaign = AdAccount(testdict['adaccount_id']).create_campaign(
            fields=fields,
            params=params,
        )
        session['campid'] = newcampaign["id"]  # save campaign id in session

        # create adset
        fields = [
        ]
        params = {
          'name': 'audience',
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
          'promoted_object': {'page_id': testdict['page_id']}, # get from session storage
        }
        newadset = AdAccount(testdict['adaccount_id']).create_ad_set(
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
                'page_id':testdict['page_id'],
                'link_data': {
                    'message': testdict['adtext'],
                    'link': 'http://fb.me/',
                    'image_hash': testdict['image_hash'],
                    'name': adheadline,
                    #'caption':'WWW.ITUNES.COM',
                    #'description':'The link description',
                    #'title': adheadline,
                    'call_to_action': {
                        'type':'SIGN_UP',
                        'value': {
                            'link':'http://fb.me/',
                            'lead_gen_form_id': testdict['lead_gen_form_id']
                        }
                    }
                }
            },
        }
        #print(g.user['access_token'])
        #FacebookAdsApi.init(access_token=g.user['access_token']) # requires user access token
        newcreative = AdAccount(testdict['adaccount_id']).create_ad_creative( # requires user access token
          fields=fields,
          params=params,
        )

        return 'Done!'
    else:
        return render_template('login.html')


if __name__ == '__main__':
 app.debug = False
 port = int(os.environ.get('PORT', 5000))
 app.run(host='0.0.0.0', port=port)
