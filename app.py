from app_functions import getSoup, getStories, getFullPage

from flask import Flask


app = Flask(__name__)
baseUrl = 'https://en.wikipedia.org/wiki/'

@app.route('/')
def getDate():
	import datetime

	now = datetime.datetime.now()
	return getFullPage(baseUrl, now.strftime('%B_%d'))

@app.route('/r')
@app.route('/random')
def random():
	return getFullPage(baseUrl, 'Special:Random')

@app.route('/page/<article>')
def exact(article):
	return getFullPage(baseUrl, article)

if __name__ == '__main__':
	app.run(debug=True)
