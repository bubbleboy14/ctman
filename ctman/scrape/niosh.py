import os, string
from cantools.web import fetch
from cantools.util import log, mkdir, read, write

IURL = "https://www.cdc.gov/niosh/npg/npgsyn-%s.html"
CURL = "https://www.cdc.gov/niosh/npg/npgd%s.html"
NDIR = os.path.join("scrape", "niosh")
FULL = os.path.join(NDIR, "full")
INDEX = os.path.join(FULL, "index")
CHEMS = os.path.join(FULL, "chems")

class Scraper(object):
	def __init__(self):
		for p in [NDIR, FULL, INDEX, CHEMS]:
			if not os.path.isdir(p):
				mkdir(p)
		self.pages = {
			"index": [],
			"chems": []
		}
		self.download()
		self.process()

	def acquire(self, url, path):
		fname = url.split("/").pop()
		fpath = os.path.join(path, fname)
		if os.path.exists(fpath):
			return read(fpath)
		data = fetch(url)
		write(data, fpath)
		return data

	def index(self):
		for letter in string.lowercase:
			self.pages["index"].append(self.acquire(IURL%(letter,), INDEX))

	def clist(self, page):
		return [CURL%(p.split("'")[0],) for p in page.split("href='npgd")[1:]]

	def chems(self):
		for page in self.pages["index"]:
			for url in self.clist(page):
				self.pages["chems"].append(self.acquire(url, CHEMS))

	def download(self):
		self.index()
		self.chems()

	def chem(self, page):
		pass # process chem page

	def process(self):
		for page in self.pages["chems"]:
			self.chem(page)