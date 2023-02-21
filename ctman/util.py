import os, magic
from cantools import config
from cantools.util import sym, cmd, log

def symage(path):
	ext = magic.from_file(path).split(" ").pop(0).lower()
	if ext not in ["png", "jpeg"]:
		log("converting %s to png!"%(ext,))
		cmd("convert -append -alpha off %s %s.png"%(path, path))
		cmd("mv %s.png %s"%(path, path))
		ext = "png"
	sname = "%s.%s"%(path.replace("blob", "build"), ext)
	if not os.path.exists(sname):
		sym("../%s"%(path,), sname)
	return sname

def getstart(h, sflag):
	i = h.find(sflag)
	while h.find(sflag, i + 1) != -1:
		i = h.find(sflag, i + 1)
	return i

panflags = {}
def panflag(src, dest, flag=None, val=None):
	if src not in panflags:
		panflags[src] = {}
	if dest not in panflags[src]:
		panflags[src][dest] = {}
	pfz = panflags[src][dest]
	if not flag:
		return pfz
	if not val:
		return pfz.get(flag)
	pfz[flag] = val

def pan(fp, ex=None, srcex="html", opath=None):
	opath = opath or "%s.%s"%(fp, ex)
	cline = 'pandoc "%s.%s" -o "%s" --verbose'%(fp, srcex, opath)
	pfz = panflag(srcex, ex)
	for k, v in pfz.items():
		cline = "%s -%s %s"%(cline, k, v)
	cmd(cline)
	return opath

def h2l(h, depth=0):
	from ctman import trans
	if config.ctman and config.ctman.legacyh2l:
		return trans.legacy.h2l(h, depth)
	return trans.html2latex.H2L(h, depth).translate()

def h2x(h):
	from ctman import trans
	return trans.html2docx.H2X(h).translate()