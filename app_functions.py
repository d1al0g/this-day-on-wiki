from bs4 import BeautifulSoup as Bs
import requests

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
