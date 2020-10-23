import os, magic
from cantools import config
from cantools.util import sym, cmd, log
from ctman.trans.html2latex import H2L

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

def h2l(h, depth=0):
	if config.ctman and config.ctman.legacyh2l:
		return trans.legacy.h2l(h, depth)
	return trans.html2latex.H2L(h, depth).translate()