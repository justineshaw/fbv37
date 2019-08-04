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


x = {'error': {'message': 'Invalid parameter', 'type': 'OAuthException', 'code': 100, 'error_subcode': 1885183, 'is_transient': False, 'error_user_title': 'Ads creative post was created by an app that is in development mode', 'error_user_msg': 'Ads creative post was created by an app that is in development mode. It must be in public to create this ad.', 'fbtrace_id': 'ANHwt5NNdbQaQkNycNwbUV4'}}
print(x)
print(x['error']['error_user_msg'])
print(x.error.error_user_msg)

acess_token="EAAFhpQB0HY0BADUkGgcS6yscyqkPKWrqOfC4JTtlAnPIXGoW0EEx9elsMUVauqyTVjX4dyYlZCcg52YKIXnqUGfiuPqUIN8RhPCvBR7cKjWa5B68pv9YT4oaM3X4Ls9LKKy6Ml1vKOOLaAgqLZAWH8Q1Vk5Hy58h9lfOhacto3X5kGoy7b3IczWBegZBmYZBwuEMsDMZBZACtWD1gyKryk"
FacebookAdsApi.init(access_token=acess_token, api_version='v3.3')

try:
    #print(1/0)
    campaign = AdAccount(id).create_campaign()
    print('all good')
except FacebookError as e:
    #print(e.get_message())
    print(e.api_error_message())
except Exception as e:
    print('error')
    if e in FacebookRequestError:
        print("hello")


'''
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
'''
