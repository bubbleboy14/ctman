from cantools.util import log

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
	"incompatibilities_and_reactivities",
	"exposure_routes", "symptoms", "target_organs",
	"respirator_recommendations"]
HCARDS = ["exposure_limits", "measurement_methods", "first_aid"]

class Chem(object):
	def __init__(self, code, page):
		self.code = code
		self.page = page
		self.data = {}
		self.scrape()

	def extract(self, f, start=None, t="</div>", unquote=True):
		s = self.page.index(f, start) + len(f)
		bit = self.page[s : self.page.index(t, s)]
		if unquote and '"' in bit:
			bit = bit.split('"')[1]
		return bit.strip()

	def card(self, flag, unquote=True, cflag='card-text">'):
		log(flag)
		return self.extract(cflag, self.page.index(flag), unquote=unquote)

	def tcard(self, flag, unquote=True):
		flag = flag.replace("_", " ").title()
		flag = flag.replace(" And ", " &amp; ")
		return self.card(flag, unquote=unquote)

	def classification(self):
		previtem = self.page.index("Lower Explosive Limit")
		classrow = self.page.index('class="row"', previtem)
		return self.extract('card-text">', classrow)

	def scrape(self):
		self.data["name"] = self.extract("<h1>", t="<")
		log("%s %s"%(self.code, self.data["name"]), important=True)
		self.data["classification"] = self.classification()
		self.data["personal_protection_sanitation"] = self.card("Personal Protection/Sanitation",
			False, 'card-body">')
		for name, flag in CARDS.items():
			self.data[name] = self.card(flag)
		for name in TCARDS:
			self.data[name] = self.tcard(name)
		for name in HCARDS:
			self.data[name] = self.tcard(name, False)