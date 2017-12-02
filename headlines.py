# -*- coding: utf-8 -*-

import feedparser
import json
import urllib
import urllib2

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1b9129a11f4310eb2020dcbc586532f9"

DEFAULTS = {'publication': 'bbc',
            'city': 'Sragen,ID'}


@app.route('/', methods=['GET', 'POST'])
def home():
    # get customized headlines based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {'description': parsed['weather'][0]['description'],
                    'temperature': parsed['main']['temp'],
                    'city': parsed['name'],
                }
    return weather



if __name__ == '__main__':
    app.run(port=5000, debug=True)
