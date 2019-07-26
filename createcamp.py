# https://developers.facebook.com/docs/marketing-api/buying-api

from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.adobjects.targeting import Targeting
import datetime
import os

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
params = {
  'name': 'Does this work?',
  'objective': 'LINK_CLICKS',
  'status': 'PAUSED',
}
newcampaign = AdAccount(id).create_campaign(
  fields=fields,
  params=params,
)

print(newcampaign["id"])

params = {
    'q': 'baseball',
    'type': 'adinterest',
}

resp = TargetingSearch.search(params=params)
# print(resp[1])

targeting = {
    Targeting.Field.geo_locations: {
        Targeting.Field.countries: ['US'],
    },
    Targeting.Field.interests: [{'id':resp[1]["id"],'name':resp[1]["name"]}]  # https://developers.facebook.com/docs/marketing-api/buying-api/targeting#interests
}
# print(targeting)


# create ad set - v2.0 - https://github.com/facebook/facebook-python-business-sdk/blob/master/examples/AdAccountAdSetsPostReach.py
fields = [
]
params = {
  'name': 'My Reach Ad Set',
  'optimization_goal': 'REACH',
  'billing_event': 'IMPRESSIONS',
  'bid_amount': '2',
  'daily_budget': '1000',
  'campaign_id': newcampaign["id"],
  'targeting': {'excluded_geo_locations':{'regions':[{'key':'3847'}]},'geo_locations':{'countries':['US']}},
  'status': 'PAUSED',
  'promoted_object': {'page_id':'1775351279446344'},
}
print (AdAccount(id).create_ad_set(
  fields=fields,
  params=params,
))

# get available images from an existing ad account
account = AdAccount(id)
images = account.get_ad_images()
print(images[5]["hash"])

# create ad
# hash image
from facebook_business.adobjects.adimage import AdImage

image = AdImage(parent_id=id)
image[AdImage.Field.filename] = '/Users/justinshaw/Documents/herokuApps/fbapp01/image1.jpeg'
image.remote_create()

# Output image Hash
print(image[AdImage.Field.hash])


#continue creating ad
fields = [
]
params = {
  'name': 'Sample Creative',
  'object_story_spec': {'page_id': '1775351279446344','link_data':{'image_hash':images[5]["hash"],'link':'https://facebook.com/1775351279446344','message':'try it out'}},
}
print (AdAccount(id).create_ad_creative(
  fields=fields,
  params=params,
))
