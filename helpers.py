import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from facebook import GraphAPI

def extend(access_token, FB_APP_ID, FB_APP_SECRET):
    print("inside extend")
    graph = GraphAPI(access_token).extend_access_token(FB_APP_ID, FB_APP_SECRET)
    return graph["access_token"]

def get_page_access_token(access_token):
    graph = GraphAPI(access_token=access_token)
    pages_data = graph.get_object("/me/accounts")
    print(pages_data)
    page_access_token = pages_data['data'][0]['access_token']  # https://medium.com/@DrGabrielA81/python-how-making-facebook-api-calls-using-facebook-sdk-ea18bec973c8
    #page_id = pages_data['data'][0]['id']  # page_id
    #session['page_access_token'] = page_access_token
    #session['page_id'] = page_id
    return page_access_token

def get_page_access_token(access_token, page_id):
    graph = GraphAPI(access_token=access_token)
    pages_data = graph.get_object("/me/accounts")
    page_access_token = pages_data['data'][0]['access_token']  # https://medium.com/@DrGabrielA81/python-how-making-facebook-api-calls-using-facebook-sdk-ea18bec973c8
    #page_id = pages_data['data'][0]['id']  # page_id
    #session['page_access_token'] = page_access_token
    #session['page_id'] = page_id
    return page_access_token

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
