import re
import requests
from bs4 import BeautifulSoup

from .text_format import *


def reformat_text(text):
	for before, after in format_chars:
		text = text.replace(before, after)

	for pattern, new in format_invalid:
		text = re.sub(pattern, new, text)

	for balise, new in format_balises_names:
		text = re.sub(balise_pattern.format(balise), new, text)

	return text


class FranceInfo:

	def __init__(self, pages_limit=None):
		self._source = "https://www.francetvinfo.fr"
		self._articles_brut = self._get_artciles(self._source)
		self._articles = self._get_artciles_formated(self._articles_brut)


	def _get_artciles(url):
		req = requests.get(url)
		data = BeautifulSoup(req.content, features="html.parser")
		data = data.findAll("article", {"data-vr-contentbox": ""})
		
		artciles = {}

		index = 0
		for d in data_list:
			links = d.findAll('a')
			
			if len(links) < 2:
				continue

			title = links[1].text
			source = links[1].get('href')
			if source != None and title != None:

				artciles[index] = {
					'title': reformat_text(title),
					'source': url + source if not source.startswith('https') else source
				}

				index += 1

		return artciles


	def _get_artciles_formated(self):
		for i, article in enumerate(self.artciles):
			data = {}

			req = requests.get(data[index]['source'])
			data = BeautifulSoup(req.content, features="html.parser")


			title = data.find("h1", {"class": "page-content content"})
			title = data.find('span', {"class": "c-title__main"}).text

			try:
				intro = reformat_text(data.find('div', {"class": "c-chapo"}).text)
			except:
				intro = ''

			try:
				time = data.find('span', {"class": "publication-date__published"})
				time = 'Publié ' + time.find('time').text
			except:
				time = None

			try:
				image = data.find('div', {"class": "c-cover--media"})
				image = image.find('picture', {"class": "picture-wrapper"})
				image = image.find('img')
				image = image.get('src')
			except:
				image = None

			try:
				paragraph = data.find('div', {"class": "c-body"})
				paragraphs = paragraph.findAll('p')
				paragraphs = [self._paragraph_reformat(p) for p in paragraphs]
			except:
				paragraphs = []

			data[i] = {
				'title':		title,
				'intro':		intro,
				'time':			time,
				'image':		image,
				'paragraphs':	paragraphs
			}
		return data


	def _paragraph_reformat(self, paragraph):
		links = paragraph.findAll('a')
		rep = {}

		for l in links:
			link = self._link(l.get('href'))
			text = l.text

			rep[str(l)] = f"[{text}]({link})"

		for key in rep:
			paragraph = paragraph.replace(key, rep[key])

		return reformat_text(paragraph)


	def _link(self, l):
		return l if l.startswith('https') else self._source + l

	
	def __len__(self):
		"""
		Return len of self._articles
		Which coresponf to the number of articles on <self._source>
		"""
		return len(self._articles)


	@property
	def source(self):
		"""
		Return self._source

		Which is <https://www.francetvinfo.fr>
		"""
		return self._source


	@property
	def articles(self):
		"""
		Return self._articles:
			List of Dicts with indexes:
		(FranceInfo.artciles[0] will always be 'la une')

		title 		:	article title
		intro		:	article introduction text
		time 		:	the release time for this article
		image		:	image related to this article
		paragraphs	:	all the paragraphs
		"""
		return self._articles

	@property
	def articles_brut(self):
		"""
		Return self._articles_brut:
			List of Dicts with indexes:
		-	title	:	article title
		-	source 	:	link to the article page

		"""
		return self._articles_brut


	def article(self, index):
		try:
			return self._articles[index]
		except IndexError:
			raise IndexError(
				f"arg index not in range 0 <= index <= {len(self._articles)}")