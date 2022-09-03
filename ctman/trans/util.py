from ctman.util import getstart
from .html2latex.rules import flags, styles, cstyles
from .html2latex.fragment import Fragment

#
# misc
#

def nextlast(h, flagz):
	f = None
	i = -1
	for flag in flagz:
		startflag = flagz[flag].get("start")
		if startflag:
			sflags = [startflag]
		else:
			sflags = ["<%s "%(flag,), "<%s>"%(flag,)]
		for sflag in sflags:
			fi = getstart(h, sflag)
			if fi > i:
				i = fi
				f = flag
	return f

def trans(h, flag, rules=None, styles=styles, cstyles=cstyles):
	rules = rules or flags[flag]
#	sflag = rules.get("start", "<%s"%(flag,))
	sflag = rules.get("start")
	altstart = None
	if not sflag:
		sflag = "<%s>"%(flag,)
		altstart = "<%s "%(flag,)
	seflag = rules.get("startend", ">")
	esflag = rules.get("endstart")
	eflag = rules.get("end", "</%s>"%(flag,))
	tex = rules.get("tex")
	while sflag in h or altstart and altstart in h:
		start = getstart(h, sflag)
		if altstart:
			start = max(start, getstart(h, altstart))
		startend = seflag and h.index(seflag, start)
		startender = (startend or start) + len(seflag or sflag)
		endstart = esflag and h.index(esflag, startender)
		end = h.index(eflag, startender or start)
		starter = h[start : startender]
		seg = h[startender : (endstart or end)]
		h = h[:start] + Fragment(seg, starter, rules, styles, cstyles).translate() + h[end + len(eflag):]
	return h

class Converter(object):
	def __init__(self, fragment, depth=0, swappers={}, flaggers={}, styles={}, cstyles={}):
		self.fragment = fragment
		self.depth = depth
		self.swappers = swappers
		self.flaggers = flaggers
		self.styles = styles
		self.cstyles = cstyles
		self.uncomment()

	def uncomment(self):
		cs = "<!--"
		ce = "-->"
		while cs in self.fragment:
			start = self.fragment.index(cs)
			end = self.fragment.index(ce, start)
			self.fragment = self.fragment[:start] + self.fragment[end + 3:]

	def translate(self):
		self.swapem()
		self.bottomsup()
		self.cleanup()
		return self.translation

	def swapem(self):
		h = self.fragment
		for swap in self.swappers:
			h = h.replace(swap, self.swappers[swap])
		self.translation = h

	def bottomsup(self):
		h = self.translation
		flag = nextlast(h, self.flaggers)
		while flag:
			h = trans(h, flag, styles=self.styles, cstyles=self.cstyles)
			flag = nextlast(h, self.flaggers)
		self.translation = h

	def cleanup(self):
		pass