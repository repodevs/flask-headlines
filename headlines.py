# -*- coding: utf-8 -*-

import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}


@app.route('/')
@app.route('/<publication>')
def get_news(publication='bbc'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    title = unicode(first_article.get('title').encode('utf8'), 'utf8') if first_article.get('title') else None
    published = unicode(first_article.get('published').encode('utf8'), 'utf8') if first_article.get('published') else None
    summary = unicode(first_article.get('summary').encode('utf8'), 'utf8') if first_article.get('summary') else None
    return render_template("home.html",
                            title=title,
                            published=published,
                            summary=summary)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
