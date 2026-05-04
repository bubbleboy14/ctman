from fyg.util import confirm, Loggy
from model import *

class Auditor(Loggy):
	def audit(self):
		self.log("audit")
		self.chemicals()
		self.templates()
		self.log("goodbye!")

	def chemicals(self):
		if not confirm("audit chemicals"):
			return
		chems = Chemical.query().all()
		names = {}
		codes = {}
		for c in chems:
			if c.name not in names:
				names[c.name] = []
			names[c.name].append(c)
			if c.code not in codes:
				codes[c.code] = []
			codes[c.code].append(c)
		for name in names:
			count = len(names[name])
			if count > 1:
				self.log("name", name, ":", count)
		for code in codes:
			count = len(codes[code])
			if count > 1:
				self.log("code", code, ":", count)

	def templates(self):
		if not confirm("audit templates"):
			return
		temps = Template.query().all()
		probs = []
		for t in temps:
			try:
				t.unrolled()
			except:
				self.log("unroll failed:", t.name)
				probs.append(t)
		if not probs:
			return self.log("you're good to go!")
		if confirm("repair %s problem templates"%(len(probs),)):
			for t in probs:
				goodsecs = []
				for s in t.sections:
					if s.get():
						goodsecs.append(s)
					else:
						self.log("can't find", s.urlsafe())
				t.sections = goodsecs
			if confirm("remove references to missing sections"):
				db.put_multi(probs)
				self.log("ok, we did it!")

def audit():
	Auditor().audit()