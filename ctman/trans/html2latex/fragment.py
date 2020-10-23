from ctman.util import symage
from .rules import styles, cstyles

class Fragment(object):
	def __init__(self, fragment, starter, rules):
		self.fragment = fragment
		self.starter = starter
		self.rules = rules

	def style(self, tx):
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
		seg = self.fragment
		if "handler" in self.rules:
			tx = self.rules["handler"](seg)
		elif "liner" in rules:
			lines = seg.strip().split("</li>")
			epart = lines.pop().replace("-", "    -")
			mdblock = "\n".join([self.rules["liner"]%(s.split(">", 1)[1],) for s in lines])
			tx = "\n%s\n%s\n"%(mdblock, epart)
		else:
			if flag == "img":
				seg = symage(seg)
			tx = self.rules.get("tex")%(seg,)
		return self.style(tx)