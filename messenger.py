# messenger.py

# from facebook_business.adobjects.adcreative import AdCreative
import os

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adaccount import AdAccount


# log in info
access_token = os.environ["USER_ACCESS_TOKEN"]
app_secret = os.environ["APP_SECRET"]
app_id = '342529826361699'
id = 'act_804097463107225' # Justin Shaw ad account is 'act_804097463107225', test ad account is 'act_255618438702332'
page_id:'1775351279446344' # Shaw Marketing page id
FacebookAdsApi.init(account_id=id, access_token=access_token)



#create campaign
fields = [
]
params ={
    'name': "Messenger Campaign 1",
    'objective': "MESSAGES",
    'status': "PAUSED",
}
newcampaign = AdAccount(id).create_campaign(
    fields=fields,
    params=params,
)
print(newcampaign)



# create ad set - v2.0 - https://github.com/facebook/facebook-python-business-sdk/blob/master/examples/AdAccountAdSetsPostReach.py
fields = [
]
params = { # https://developers.facebook.com/docs/marketing-api/reference/ad-campaign
  'name': 'My Reach Ad Set',
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
  'promoted_object': {'page_id':'1775351279446344'},
}
newadset = AdAccount(id).create_ad_set(
  fields=fields,
  params=params,
)
print(newadset["id"])




# create ad
fields = [
]
params = {
  'name': 'My Ad',
  'adset_id': newadset["id"],
  'creative': {'creative_id': '23843808299800536'}, # to get the creative associated with an exiting ad use: "23843808299510536/adcreatives", where first number is ad id, which can be found in ad manager stats
  'status': 'PAUSED',
}
print (AdAccount(id).create_ad(
  fields=fields,
  params=params,
))
