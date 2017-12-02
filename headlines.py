# -*- coding: utf-8 -*-

import feedparser
from flask import Flask


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
    title = first_article.get('title').encode('utf8') if first_article.get('title') else None
    published = first_article.get('published').encode('utf8') if first_article.get('published') else None
    summary = first_article.get('summary').encode('utf8') if first_article.get('summary') else None
    return """<html>
        <body>
            <h1> HEADLINES </h1>
            <b>{0}</b> <br />
            <i>{1}</i> <br />
            <p>{2}</p> <br />
        </body>
    </html>""".format(title, published, summary)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
