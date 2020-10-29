import os, string
from cantools.web import fetch
from cantools.util import log, mkdir, read, write
from ctman.scrape.niosh.chemical import Chem
from model import db, Chemical

IURL = "https://www.cdc.gov/niosh/npg/npgsyn-%s.html"
CURL = "https://www.cdc.gov/niosh/npg/npgd%s.html"
NDIR = os.path.join("scrape", "niosh")
INDEX = os.path.join(NDIR, "index")
CHEMS = os.path.join(NDIR, "chems")

class Scraper(object):
	def __init__(self):
		log("initializing niosh scraper")
		for p in [NDIR, INDEX, CHEMS]:
			if not os.path.isdir(p):
				mkdir(p)
		self.pages = {
			"index": [],
			"chems": []
		}
		self.chemcodes = []
		self.chemicals = []
		self.download()
		self.process()
		self.save()
		log("scrape complete")

	def save(self):
		log("creating %s Chemical records"%(len(self.chemicals),))
		puts = []
		for chem in self.chemicals:
			puts.append(Chemical(**chem))
		log("saving %s Chemical records"%(len(puts),))
		db.put_multi(puts)

	def acquire(self, url, path):
		fname = url.split("/").pop()
		fpath = os.path.join(path, fname)
		if os.path.exists(fpath):
			return read(fpath)
		log("acquiring: %s"%(url,))
		data = fetch(url)
		write(data, fpath)
		return data

	def index(self):
		for letter in string.lowercase:
			self.pages["index"].append(self.acquire(IURL%(letter,), INDEX))

	def clist(self, page):
		return [p.split(".")[0] for p in page.split("href='npgd")[1:]]

	def chems(self):
		pages = self.pages["index"]
		log("scanning %s index pages"%(len(pages),), important=True)
		for page in pages:
			chemcodes = self.clist(page)
			self.chemcodes += chemcodes
			log("found %s chem pages"%(len(chemcodes),))
			for code in chemcodes:
				self.pages["chems"].append(self.acquire(CURL%(code,), CHEMS))

	def download(self):
		log("downloading", important=True)
		self.index()
		self.chems()

	def process(self):
		pages = self.pages["chems"]
		lp = len(pages)
		log("processing %s chemical pages"%(lp,), important=True)
		for i in range(lp):
			self.chemicals.append(Chem(self.chemcodes[i], pages[i]).data)