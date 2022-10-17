from ctman.util import getstart
from .html2latex.rules import flags, styles, cstyles
from .fragment import Fragment

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

def trans(h, flag, rules=None, flags=flags, styles=styles, cstyles=cstyles):
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
	def __init__(self, fragment, depth=0, swappers={}, flaggers={}, styles={}, cstyles={}, linestrips=[], loud=False):
		self.fragment = fragment
		self.depth = depth
		self.swappers = swappers
		self.flaggers = flaggers
		self.styles = styles
		self.cstyles = cstyles
		self.linestrips = linestrips
		self.loud = loud
		self.uncomment()
		linestrips and self.striplines()

	def log(self, *msg):
		self.loud and print(*msg)

	def striplines(self):
		lines = []
		for line in self.fragment.split("\n"):
			for flag in self.linestrips:
				if flag in line:
					lines.append(flag)
				else:
					lines.append(line)
		self.fragment = "\n".join(lines)

	def uncomment(self):
		cs = "<!--"
		ce = "-->"
		while cs in self.fragment:
			start = self.fragment.index(cs)
			end = self.fragment.index(ce, start)
			self.fragment = self.fragment[:start] + self.fragment[end + 3:]

	def translate(self):
		self.swapem()
		self.log("\n======================\n", "prebot", self.translation[:200], "\n======================\n")
		self.bottomsup()
		self.log("\n======================\n", "preclean", self.translation[:200], "\n======================\n")
		self.cleanup()
		self.log("\n======================\n", "postclean", self.translation[:200], "\n======================\n")
		return self.translation

	def swapem(self):
		h = self.fragment
		for swap in self.swappers:
			swapper = self.swappers[swap]
			self.log("swapping", swap, "for", swapper)
			h = h.replace(swap, swapper)
		self.translation = h

	def bottomsup(self):
		h = self.translation
		flag = nextlast(h, self.flaggers)
		while flag:
			self.log("transing", flag)
			h = trans(h, flag, flags=self.flaggers, styles=self.styles, cstyles=self.cstyles)
			flag = nextlast(h, self.flaggers)
		self.translation = h

	def cleanup(self):
		pass