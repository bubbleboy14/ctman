from ctman.util import symage
from .rules import styles, cstyles

class Fragment(object):
	def __init__(self, fragment, starter, rules, styles=styles, cstyles=cstyles):
		self.fragment = fragment
		self.starter = starter
		self.rules = rules
		self.styles = styles
		self.cstyles = cstyles
		self.realign()

	def realign(self):
		aligner = ' align="'
		if not aligner in self.starter: return
		alignment = self.starter.split(aligner).pop().split('"').pop(0)
		stysta = ' style="'
		sta = '%stext-align: %s;'%(stysta, alignment)
		if "style" in self.starter:
			self.starter = self.starter.replace(stysta, '%s '%(sta,))
		else:
			self.starter = self.starter.replace('%s%s"'%(aligner, alignment), '%s"'%(sta,))

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
					tx = self.styles[key][val]%(tx,)
			elif key in self.cstyles:
				tx = self.cstyles[key]%(val[-6:], tx)
		return tx

	def translate(self):
		seg = self.style(self.fragment)
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