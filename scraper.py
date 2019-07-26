#https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import g, Flask, flash, jsonify, redirect, render_template, request, session
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.user import User


def scraper(query_address):
    '''
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

    # query the website and return the html to the variable ‘page’
    request = urllib.request.Request(url, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(request)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(response, 'html.parser')

    #g et the address
    address_box = soup.find('div', attrs={'class': 'small-12 columns prop-address'})
    address = address_box.text.strip() # strip() is used to remove starting and trailing


    # find the area on the page with the price, beds, baths, and sqft I want from the soup element
    details_box = soup.find('div', attrs={'class': 'small-12 columns show-for-medium-up prop-sup-details'})

    # hone in on the area
    target = details_box.dl
    values = target.find_all('dd') #get all the 'dd' elements in the parent object

    # store all elements
    property_details = {
        'price': values[0].text.strip(),
        'bed': values[1].text.strip(),
        'bath': values[2].text.strip(),
        'sqft': values[3].text.strip(),
        'address': address
    }


    # convert price to 4XX,XXX format
    # get city from address, returns CITY (in all caps)
    # has image function (requires fb function so add to main application?)
    '''

    #declare a dict to store all the variables
    property_details = {}

    # user types in the address in the search query box and it's matched to a google address
    property_details['query_address'] = '1315 Center Lake Drive, Mount Pleasant, SC 29464'
    property_details['query_city'] = 'Charleston'
    property_details['query_city'] = property_details['query_city'].upper()  # uppercase all letters in city
    '''
    # find a partner site based on city(5000) or state (50)
    if property_details['query_city'] == "Charleston" or "Mount Pleasant": # in V2, have a scraper db with key value pairs to match address with partner site
        property_details['partner_site'] = 'deleted for privacy'
    search the partner_site for property specific url using the query_address and return it to scrape
        property_details['scraped_url'] = 'deleted for privacy'
    '''

    #scraper returns the following values

# Adding a new key value pair
    property_details.update ({ # retrieved from website and add to db
        'price': '$400,000',
        'beds': '3',
        'baths': '3',
        'sqft': '1500',
        'scraped_address': '1315 Center Lake Drive, Mount Pleasant, SC 29464',
        'scraped_image': 'https://t.realgeeks.media/thumbnail/LSsbogr5NtKyMMN5PUUqjiVv98w=/trim:top-left:50/https://property-media.realgeeks.com/101/40de1f38333c75fe778e90a32241050b.jpg',
    })
    return property_details


def hash(img_url, adaccount_id, access_token): # hash user inputted image
    fields = [
    ]
    params ={
        #'filename': 'static/demoad1.png',
        'filename': img_url,
        'parent_id': adaccount_id, #'act_123',
    }
    image = AdImage(adaccount_id).api_create( # need access token - user or page?
        parent_id= adaccount_id,
        params= params,
    )
    print(image)
    hash = image['hash']
    return hash

def get_adaccounts():  # get users ad accounts using the user_id and access_token above
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
    # added to database table as default
        # page_id: "1775351279446344"
        # first adaccount_id - 'act_804097463107225',
        # first adaccount_name - 'Justin Shaw'
        # lead_gen_form_id - ""
        # privacy_policy_url - ""
        # property_url - ""
        # budget - defaults to number 5
        # duration - defaults to number 3

    return property_details

#url = 'deleted for privacy'
#scraper(url)
