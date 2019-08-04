@app.route('/publish_ad', methods=['POST'])
def publish_ad():
#publish_ad.py is the definitive workflow to publish a facebook ad given all the necessary paramaters

# Reference for Creating A Lead Ad: https://developers.facebook.com/docs/marketing-api/guides/lead-ads/create#creating-ad

# initialize object with page_access_token from user selected page
# set ad_account equal to user selected ad_account
# set page_id equal to user selected page
# set url equal to user selected landing page
# privacy_policy = "https://fbapp0111.herokuapp.com/terms" # what if app users could all use the same privacy policy that I host on the app
# set message equal to user inputted ad message
# set image_hash equal to result of call to get_image_hash helper function
# set headline equal to user inputted headline

# if leadgen_tos_accepted == False,
    # accept terms on behalf of user? https://www.facebook.com/ads/leadgen/tos
    # popup for user to accept terms of service
    # here's a reference for the leadgen_tos_accepted parameter: https://developers.facebook.com/docs/graph-api/reference/page#Reading

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

    fields = [
    ]
    params = {
      'name': "Ad Set Name Placeholder",
      'optimization_goal': 'LEAD_GENERATION', #or LINK_CLICKS
      'billing_event': 'IMPRESSIONS',
      'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
      'daily_budget': '100', # $1
      'campaign_id': campaign["id"],
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
      'name': "Form Name Placeholder",
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
     ''' # customizing the thank_you_page is optional
    "thank_you_page": {
      "title": "Great! You're All Set.",
      "body": "Feel free to access the property info below now.",
      "button_text": "View Property Details",
      "enable_messenger": False,
      "button_type": "VIEW_WEBSITE",
      "website_url": "https://fbapp0111.herokuapp.com/",
      },
      '''
     # "leadgen_tos_accepted": True
    }
    #FacebookAdsApi.init(access_token=session['page_access_token'])
    lead_gen_form = (Page(page_id).create_lead_gen_form( # ABC realty  page_id: 218711598949970 shaw marketing page_id: #1775351279446344
      fields=fields,
      params=params,
    ))

# Step 4: create a creative
    # call helper method to hash user inputted image

    fields = [
    ]
    params = {
        'object_story_spec': {
            'page_id': page_id,
            'link_data': {
                'message': message,
                'link': 'http://fb.me/',
                'image_hash': image_hash,
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
