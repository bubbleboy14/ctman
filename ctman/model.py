from datetime import datetime, timedelta
from fyg.util import confirm
from cantools import db, config
from cantools.util import log, error
from cantools.web import send_mail, email_admins
from ctuser.model import *
from ctedit.model import PageEdit, Style
from ctman.util import h2l, symage

class Member(CTUser):
	expiration = db.DateTime()

	def onsale(self, amount, errmsg=None):
		days = config.ctman.subs[amount]
		payment = Payment(member=self.key,
			amount=amount, duration=days)
		if errmsg:
			payment.message = errmsg
			return payment.put()
		payment.successful = True
		if not self.expiration:
			self.expiration = datetime.now()
		self.expiration += timedelta(days)
		db.put_multi([self, payment])
		exp = str(self.expiration)[:19]
		send_mail(to=self.email, subject="your subscription",
			body="your subscription is good until %s"%(exp,))
		email_admins("new subscription", "\n".join([
			"member: " + self.email,
			"amount: " + amount,
			"expires: " + exp
		]))
		return exp

class Payment(db.TimeStampedBase):
	member = db.ForeignKey(kind=Member)
	successful = db.Boolean(default=False)
	amount = db.String()
	duration = db.Integer() # days
	message = db.Text()

class SecBase(db.TimeStampedBase):
	name = db.String()
	description = db.Text()
	sections = db.ForeignKey(kind="section", repeated=True)

	def secs(self, sections=None, depth=0, novars=False, page_breaks=False):
		return "\r\n\r\n".join(sections and [
			db.get(s['key']).content(s['sections'],
				depth, novars, page_breaks) for s in sections
		] or [
			s.content(depth=depth, novars=novars,
				page_breaks=page_breaks) for s in db.get_multi(self.sections)
		])

	def fixed_desc(self, depth=0, novars=False):
		d = self.description
		return h2l(novars and d.replace("{{", "(").replace("}}", ")") or d, depth)

	def desc(self, depth=0, novars=False):
		return self.fixed_desc(depth, novars)

	def header(self):
		return self.name

	def body(self, depth, novars=False, page_breaks=False):
		tline = "%s %s"%("#" * depth, self.header())
		if page_breaks and depth == 1:
			tline = "\\newpage%s"%(tline,)
		return "%s\r\n\r\n%s"%(tline, self.desc(depth, novars))

	def content(self, sections=None, depth=0, novars=False, page_breaks=False):
		body = self.body(depth, novars, page_breaks)
		secs = self.sections and self.secs(sections,
			depth + 1, novars, page_breaks) or ""
		cont = "%s\r\n\r\n%s"%(body, secs)
		log(cont)
		return cont

	def unrolled(self):
		d = self.data()
		d['sections'] = [s.unrolled() for s in db.get_multi(self.sections)]
		return d

class Section(SecBase):
	image = db.Binary()
	headerless = db.Boolean(default=False)
	landscape = db.Boolean(default=False)

	def embedders(self):
		return SecBase.query(SecBase.sections.contains(self.key.urlsafe())).all()

	def beforeremove(self, session):
		embedders = self.embedders()
		for embedder in embedders:
			embedder.sections = list(filter(lambda s : s != self.key, embedder.sections))
		db.put_multi(embedders, session=session)

	def labeler(self):
		return "%s [%s]"%(self.name, self.index)

	def header(self):
		return self.headerless and " " or self.name

	def landed(self, cont):
		if self.landscape:
			return "\\landscapeon\n%s\n\\landscapeoff"%(cont,)
		return cont

	def desc(self, depth=0, novars=False):
		d = self.fixed_desc(depth, novars)
		if not self.image:
			return self.landed(d)
		return self.landed("%s\r\n\r\n![](%s)"%(d, symage(self.image.path)))

class Injection(db.TimeStampedBase):
	name = db.String()
	variety = db.String(choices=["text", "text block"])
	fallback = db.String()

	def labeler(self):
		return "%s (%s)"%(self.name, self.variety)

class Template(SecBase):
	owner = db.ForeignKey(kind=Member)
	injections = db.ForeignKey(kind=Injection, repeated=True)

	def body(self, depth, novars=False, page_breaks=False):
		return self.desc(depth, novars)

class Document(db.TimeStampedBase):
	owner = db.ForeignKey(kind=Member)
	logo = db.Binary()
	template = db.ForeignKey(kind=Template)
	name = db.String()
	font = db.String()
	injections = db.JSON()
	assembly = db.JSON()
	declarations = db.JSON()
	pdf = db.String()
	revision = db.Integer(default=0)
	signup_sheet = db.Boolean(default=True)
	table_of_contents = db.Boolean(default=True)
	declaration_page = db.Boolean(default=True)
	pretty_filenames = db.Boolean(default=True)
	section_page_breaks = db.Boolean(default=False)

	def summary(self):
		d = {
			"key": self.id(),
			"name": self.name,
			"revision": self.revision,
			"pdf": self.pdf,
			"created": str(self.created)[:19],
			"modified": str(self.modified)[:19],
			"declarations": self.declarations or {}
		}
		if self.template:
			t = self.template.get()
			d["template"] = {
				"key": t.id(),
				"name": t.name
			}
		return d

	def content(self, sections=None):
		return self.template.get().content(sections,
			page_breaks=self.section_page_breaks)

class Table(db.TimeStampedBase):
	name = db.String()
	csv = db.Binary()

class Chemical(db.TimeStampedBase):
	classification = db.String()
	code = db.String()
	name = db.String()
	cas = db.String()
	rtecs = db.String()
	dot = db.String()
	idlh = db.String()
	synonyms_and_trade_names = db.String()
	formula = db.String()
	conversion = db.String()
	physical_description = db.String()
	molecular_weight = db.String()
	boiling_point = db.String()
	melting_point = db.String()
	freezing_point = db.String()
	solubility = db.String()
	vapor_pressure = db.String()
	ionization_potential = db.String()
	specific_gravity = db.String()
	flash_point = db.String()
	upper_explosive_limit = db.String()
	lower_explosive_limit = db.String()
	incompatibilities_and_reactivities = db.String()
	exposure_routes = db.String()
	symptoms = db.String()
	target_organs = db.String()
	cancer_site = db.String()
	respirator_recommendations = db.Text()
	exposure_limits = db.Text()
	measurement_methods = db.Text()
	first_aid = db.Text()
	personal_protection_sanitation = db.Text()

	def basic(self):
		return {
			"key": self.id(),
			"name": self.name
		}

class Pruner(object):
	def __init__(self, model=Chemical, props=["classification", "code", "cas", "formula", "physical_description"]):
		self.model = model
		self.props = props
		self.items = model.query().all()
		log("%s items"%(len(self.items),))
		self.nameSort()
		self.propCheck()
		self.undupe()

	def undupe(self):
		if not confirm("remove duplicates across %s names?"%(len(self.multis),)):
			return log("ok, bye!")
		for name in self.multis:
			prunes = self.multis[name][1:]
			log("pruning %s %s records"%(len(prunes), name))
			db.delete_multi(prunes)

	def propCheck(self):
		log("%s redundant names"%(len(self.multis),))
		for name in self.multis:
			items = self.names[name]
			matching = True
			for prop in self.props:
				val = getattr(items[0], prop)
				for item in items:
					if val != getattr(item, prop):
						matching = False
			if not matching:
				error("%s %s rows don't match - aborting!"%(len(items), name))
			log("%s items named %s - matching: %s"%(len(items), name, matching))

	def nameSort(self):
		self.names = {}
		for item in self.items:
			if item.name not in self.names:
				self.names[item.name] = []
			self.names[item.name].append(item)
		names = self.names.keys()
		log("%s names"%(len(names),))
		self.multis = list(filter(lambda n : len(self.names[n]) > 1, names))