#raise fb_response.error()
#facebook_business.exceptions.FacebookRequestError:

"""
All errors specific to Facebook api requests and Facebook ads design will be
subclassed from FacebookError which is subclassed from Exception.

Object order from parent to child - all classes: Exception > FacebookError > FacebookRequestError / FacebookBadObjectError / FacebookBadParameterTypeException
"""
# class FacebookError(Exception): # takes an exception and creates unique exceptions
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookError, FacebookRequestError
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.api import FacebookAdsApi
from bs4 import BeautifulSoup # webscraper

access_token = ''
app_secret = ''
app_id = ''
id = '23844161610780536'
FacebookAdsApi.init(access_token=access_token, api_version='v3.3')

fields = [
]
params = {
  'ad_format': 'MOBILE_FEED_STANDARD',
}
data = AdCreative(id).get_previews(
  fields=fields,
  params=params,
)

print(data)
soup = BeautifulSoup(data[0]['body'], 'html5lib')
iframe = soup.find_all('iframe')[0]['src']
print(iframe)
