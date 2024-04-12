from fyg.util import confirm
from cantools.web import error
from model import Chemical

PRUPROPS = ["classification", "code", "cas", "formula", "physical_description"]
LINPROPS = ["rtecs", "idlh", "respirator_recommendations", "exposure_limits",
	"measurement_methods", "first_aid", "personal_protection_sanitation"]

class Pruner(object):
	def __init__(self, items):
		self.items = items
		self.nameSort()
		self.propCheck()
		self.undupe()

	def log(self, msg):
		log("Pruner : %s"%(msg,))

	def undupe(self):
		if not confirm("remove duplicates across %s names"%(len(self.multis),)):
			return self.log("ok, bye!")
		for name in self.multis:
			prunes = self.names[name][1:]
			self.log("pruning %s %s records"%(len(prunes), name))
			db.delete_multi(prunes)

	def propCheck(self):
		self.log("%s redundant names"%(len(self.multis),))
		for name in self.multis:
			items = self.names[name]
			for prop in PRUPROPS:
				val = getattr(items[0], prop)
				for item in items:
					if val != getattr(item, prop):
						error("%s %s rows don't match - aborting!"%(len(items), name))
			self.log("%s items named %s"%(len(items), name))

	def nameSort(self):
		self.names = {}
		for item in self.items:
			if item.name not in self.names:
				self.names[item.name] = []
			self.names[item.name].append(item)
		names = self.names.keys()
		self.log("%s names"%(len(names),))
		self.multis = list(filter(lambda n : len(self.names[n]) > 1, names))

class Linker(object):
	def __init__(self, items):
		self.items = items
		self.fix()

	def log(self, msg):
		log("Linker : %s"(msg,))

	def linx(self, text):
		parts = text.split(" href")
		newparts = []
		changed = False
		for part in parts:
			sing = part.find("'")
			doub = part.find('"')
			if sing == -1:
				quote = '"'
				qindex = doub
			elif doub == -1:
				quote = "'"
				qindex = sing
			else:
				smallsing = sing < doub
				quote = smallsing and "'" or '"'
				qindex = smallsing and sing or doub
			link = part[qindex:part.find(quote, qindex + 1)]
			# TODO : if link.startswith(...)


	def fix(self):
		for item in self.items:
			for prop in LINPROPS:
				val = getattr(item, prop)
				links = self.linx(val)



class Muncher(object):
	def __init__(self, model=Chemical):
		self.items = model.query().all()
		self.log("%s items"%(len(self.items),))
		confirm("prune") and Pruner()
		confirm("fix links") and Linker()

	def log(self, msg):
		log("Muncher : %s"%(msg,))

if __name__ == "__main__":
	Muncher()