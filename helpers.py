import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from facebook import GraphAPI

def extend(access_token, FB_APP_ID, FB_APP_SECRET):
    print("inside extend")
    extended = GraphAPI(access_token).extend_access_token(FB_APP_ID, FB_APP_SECRET)
    return extended["access_token"]

def apology(message, code=400):
    return "Error"


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
