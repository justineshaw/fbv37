import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(query, time):  # returns the name, price, and symbol encapsualted within a DICT: https://www.w3schools.com/python/python_dictionaries.asp
    """Look up quote for symbol."""

    # Contact API
    try:
        # response = requests.get(f"https://api.iextrading.com/1.0/stock/{urllib.parse.quote_plus(symbol)}/quote")
        # "https://api.edamam.com/search?q=chicken&app_id=${YOUR_APP_ID}&app_key=${YOUR_APP_KEY}&from=0&to=3&calories=591-722&health=alcohol-free"
        response = requests.get(f"https://api.edamam.com/search?q={urllib.parse.quote(query)}&app_id=be3c8463&app_key=11a8fe1bb971178c651f737a1f5ae61f&from=0&to=11&time={urllib.parse.quote(time)}")

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        recipe = response.json()
        if recipe["count"] == 0:
            return None
        else:
            # return a list of recipe titles, urls, and images
            return recipe
            # return {
                # "recipeTitle": recipe["hits"][1]["recipe"]["label"],
                # "url": recipe["hits"][1]["recipe"]["url"],
                # "image": recipe["hits"][1]["recipe"]["image"]
            # }

        # quote = response.json()
        # return {
            # "name": quote["companyName"],
            # "price": float(quote["latestPrice"]),
            # "symbol": quote["symbol"]
        # }

    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
