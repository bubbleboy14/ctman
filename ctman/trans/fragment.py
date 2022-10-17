from cantools.web import strip_html, strip_html_carefully
from ctman.util import symage
from .html2latex.rules import styles, cstyles

class Fragment(object):
	def __init__(self, fragment, starter, rules, styles=styles, cstyles=cstyles, loud=False):
		self.fragment = fragment
		self.starter = starter
		self.rules = rules
		self.styles = styles
		self.cstyles = cstyles
		self.loud = loud
		self.realign()

	def log(self, *msg):
		self.loud and print(*msg)

	def repstart(self, a, b):
		self.log("swapping", a, "for", b)
		self.starter = self.starter.replace(a, b)

	def realign(self):
		aligner = ' align="'
		if not aligner in self.starter: return
		alignment = self.starter.split(aligner).pop().split('"').pop(0)
		stysta = ' style="'
		sta = '%stext-align: %s;'%(stysta, alignment)
		if "style" in self.starter:
			self.repstart(stysta, '%s '%(sta,))
		else:
			self.repstart('%s%s"'%(aligner, alignment), '%s"'%(sta,))

	def style(self, tx):
		if self.rules.get("nostyle"):
			return tx
		if "style" not in self.starter:
			return tx
		start = self.starter.index('style="') + 7
		end = self.starter.index(';"', start)
		srules = self.starter[start:end]
		for rule in srules.split("; "):
			[key, val] = rule.split(": ")
			if key in self.styles:
				if val in self.styles[key]:
					self.log("restyling from:", tx)
					tx = self.styles[key][val]%(tx,)
					self.log("to": tx)
			elif key in self.cstyles:
				self.log("restyling from:", tx)
				tx = self.cstyles[key]%(val[-6:], tx)
				self.log("to": tx)
		return tx

	def sanitize(self, seg): # mainly strip for now
		strip = self.rules.get("strip")
		if strip == True:
			seg = strip_html(seg)
		elif strip:
			seg = strip_html_carefully(seg, strip)
		sanswap = self.rules.get("sanswap")
		if sanswap:
			for k, v in sanswap.items():
				seg = seg.replace(k, v)
		return seg

	def translate(self):
		seg = self.style(self.sanitize(self.fragment))
		if "handler" in self.rules:
			return self.rules["handler"](seg)
		if "liner" in self.rules:
			lines = seg.strip().split("</li>")
			epart = lines.pop().replace("- ", "    - ")
			mdblock = "\n".join([self.rules["liner"]%(s.split(">", 1)[1].replace("- ",
				"    - "),) for s in lines])
			return "\n%s\n%s\n"%(mdblock, epart)
		if self.rules.get("sym"):
			seg = symage(seg)
		return self.rules.get("tex")%(seg,)