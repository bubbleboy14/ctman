from cantools import db
from cantools.util import log
from ctuser.model import *
from ctedit.model import PageEdit, Style
from ctman.util import h2l, symage

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

	def labeler(self):
		return "%s [%s]"%(self.name, self.index)

	def header(self):
		return self.headerless and " " or self.name

	def desc(self, depth=0, novars=False):
		d = self.fixed_desc(depth, novars)
		if not self.image:
			return d
		return "%s\r\n\r\n![](%s)"%(d, symage(self.image.path))

class Injection(db.TimeStampedBase):
	name = db.String()
	variety = db.String(choices=["text", "text block"])

	def labeler(self):
		return "%s (%s)"%(self.name, self.variety)

class Template(SecBase):
	owner = db.ForeignKey(kind=CTUser)
	injections = db.ForeignKey(kind=Injection, repeated=True)

	def body(self, depth, novars=False, page_breaks=False):
		return self.desc(depth, novars)

class Document(db.TimeStampedBase):
	owner = db.ForeignKey(kind=CTUser)
	logo = db.Binary()
	template = db.ForeignKey(kind=Template)
	name = db.String()
	injections = db.JSON()
	assembly = db.JSON()
	pdf = db.String()
	revision = db.Integer(default=0)
	signup_sheet = db.Boolean(default=True)
	table_of_contents = db.Boolean(default=True)
	pretty_filenames = db.Boolean(default=True)
	section_page_breaks = db.Boolean(default=False)

	def summary(self):
		d = {
			"key": self.id(),
			"name": self.name,
			"revision": self.revision,
			"pdf": self.pdf,
			"created": str(self.created)[:19],
			"modified": str(self.modified)[:19]
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