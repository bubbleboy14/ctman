import os, string
from cantools.web import fetch
from cantools.util import mkdir, write

IURL = "https://www.cdc.gov/niosh/npg/npgsyn-%s.html"
NDIR = os.path.join("scrape", "niosh")
FULL = os.path.join(NDIR, "full")
INDEX = os.path.join(FULL, "index")
CHEMS = os.path.join(FULL, "chems")

def acquire(url, path):
	fname = url.split("/").pop()
	fpath = os.path.join(path, fname)
	if not os.path.exists(fpath):
		data = fetch(url)
		write(data, fpath)

def index():
	for letter in string.lowercase:
		acquire(IURL%(letter,), INDEX)

def scrape():
	for p in [NDIR, FULL, INDEX, CHEMS]:
		if not os.path.isdir(p):
			mkdir(p)
	index()