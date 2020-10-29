from cantools.util import log, error

CARDS = {
	"cas": "CAS No.",
	"rtecs": "RTECS No.",
	"dot": "DOT ID &amp; Guide",
	"idlh": "IDLH"
}
TCARDS = ["synonyms_and_trade_names", "formula", "conversion",
	"physical_description", "molecular_weight", "boiling_point",
	"freezing_point", "solubility", "vapor_pressure",
	"ionization_potential", "specific_gravity", "flash_point",
	"upper_explosive_limit", "lower_explosive_limit",
	"incompatibilities_and_reactivities", "exposure_routes",
	"symptoms", "target_organs", "cancer_site"]
HCARDS = ["exposure_limits", "measurement_methods"]
BCARDS = ["Respirator Recommendations", "First Aid",
	"Personal Protection/Sanitation"]

class Chem(object):
	def __init__(self, code, page):
		self.code = code
		self.page = page.decode()
		self.data = { "code": code }
		self.scrape()

	def getstart(self, f, start=None):
		i = self.page.find(f, start)
		i2 = None
		if '"' in f:
			i2 = self.page.find(f.replace('"', "'"), start)
		elif "'" in f:
			i2 = self.page.find(f.replace("'", '"'), start)
		if i2 and i2 != -1:
			if i == -1 or i > i2:
				i = i2
		if i == -1:
			error("can't find %s"%(f,))
		return i

	def extract(self, f, start=None, t="</div>", unquote=True):
		s = self.getstart(f, start) + len(f)
		bit = self.page[s : self.page.index(t, s)]
		if unquote and '"' in bit:
			bit = bit.split('"')[1]
		return bit.strip()

	def card(self, flag, unquote=True, cflag='card-text">'):
		if flag not in self.page:
			log("%s - skipping!"%(flag,))
			return ""
		log(flag)
		return self.extract(cflag, self.page.index(flag), unquote=unquote)

	def tcard(self, flag, unquote=True):
		flag = flag.replace("_", " ").title()
		flag = flag.replace(" And ", " &amp; ")
		return self.card(flag, unquote=unquote)

	def classification(self):
		previtem = self.page.find("Lower Explosive Limit")
		if previtem == -1:
			mw = self.page.index("Molecular Weight")
			previtem = self.page.index('class="row"', mw) + 1
		classrow = self.page.index('class="row"', previtem)
		return self.extract('card-text">', classrow)

	def scrape(self):
		self.data["name"] = self.extract("<h1>", t="<")
		log("%s %s"%(self.code, self.data["name"]), important=True)
		self.data["classification"] = self.classification()
		for name, flag in CARDS.items():
			self.data[name] = self.card(flag)
		for name in TCARDS:
			self.data[name] = self.tcard(name)
		for name in HCARDS:
			self.data[name] = self.tcard(name, False)
		for name in BCARDS:
			self.data[name.lower().replace("/", " ").replace(" ",
				"_")] = self.card(name, False, 'card-body">')