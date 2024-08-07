dirs = ["build", "templates", "tex", "scrape"]
copies = {
	"tex": ["imps.tex", "pre.tex"]
}
syms = {
	".": ["_man.py", "memscan.py"],
	"css": ["man.css"],
	"html": ["man"],
	"js": ["man"]
}
model = {
	"ctman.model": ["*"]
}
routes = {
	"/_man": "_man.py",
	"/build": "build"
}
requires = ["ctuser"]
cfg = {
	"builder": {
		"verbose": False,
		"injeclarations": True
	},
	"font": {
		"family": None,
		"size": "12pt"
	},
	"toc": {
		"secheaders": False
	},
	"subs": {
		"10.00": 30,
		"100.00": 365
	}
}
dependencies = ["pandoc", "texlive-latex-base", "texlive-fonts-recommended", "texlive-extra-utils", "texlive-latex-extra", "texlive-xetex"]