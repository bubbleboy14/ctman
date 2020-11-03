from ctman.util import symage
from .rules import styles, cstyles

class Fragment(object):
	def __init__(self, fragment, starter, rules):
		self.fragment = fragment
		self.starter = starter
		self.rules = rules

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
			if key in styles:
				if val in styles[key]:
					tx = styles[key][val]%(tx,)
			elif key in cstyles:
				tx = cstyles[key]%(val[1:], tx)
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