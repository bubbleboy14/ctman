dirs = ["build", "templates", "tex"]
copies = {
	"tex": ["imps.tex", "pre.tex"]
}
syms = {
	".": ["_man.py"],
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
