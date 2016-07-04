from bs4 import BeautifulSoup as Bs
from flask import Flask, render_template
import requests

app = Flask(__name__)
baseUrl = 'https://en.wikipedia.org/wiki/'

def getSoup(baseUrl, append):
	url = baseUrl + append
	pageText = requests.get(url).text
	soup = Bs(pageText, "lxml")
	return soup

def getStories(soup):
	header = soup.find('h1', id="firstHeading").text
	summaries = soup.find("div", id="mw-content-text").find_all("p")

	def cleanStories(summaries):
		paragraphs = summaries
		for p in paragraphs:
			if p.text.isspace() or len(p.text) < 1:
				paragraphs.remove(p)
		return paragraphs

	paragraphs = [s.text for s in cleanStories(summaries)]
	return header, paragraphs

def getFullPage(baseUrl, append):
	soup = getSoup(baseUrl, append)
	header, paragraphs = getStories(soup)
	return render_template('layout.html', header=header, para=paragraphs)

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
