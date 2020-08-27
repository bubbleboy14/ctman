from cantools import db
from cantools.util import log
from ctuser.model import *
from ctedit.model import PageEdit, Style
from ctman.util import h2l

class SecBase(db.TimeStampedBase):
	name = db.String()
	description = db.Text()
	sections = db.ForeignKey(kind="section", repeated=True)

	def secs(self, sections=None, depth=1):
		return "\r\n\r\n".join(sections and [
			db.get(s['key']).content(s['sections'], depth) for s in sections
		] or [s.content(depth=depth) for s in db.get_multi(self.sections)])

	def fixed_desc(self):
		return h2l(self.description)

	def desc(self):
		return self.fixed_desc()

	def header(self):
		return self.name

	def body(self, depth):
		tline = "%s %s"%("#" * depth, self.header())
		return "%s\r\n\r\n%s"%(tline, self.desc())

	def content(self, sections=None, depth=1):
		body = self.body(depth)
		secs = self.sections and self.secs(sections, depth + 1) or ""
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

	def desc(self):
		d = self.fixed_desc()
		if not self.image:
			return d
		return "%s\r\n\r\n![](%s)"%(d, self.image.path)

class Template(SecBase):
	owner = db.ForeignKey(kind=CTUser)

class Document(db.TimeStampedBase):
	owner = db.ForeignKey(kind=CTUser)
	logo = db.Binary()
	template = db.ForeignKey(kind=Template)
	name = db.String()
	injections = db.JSON()
	assembly = db.JSON()
	pdf = db.String()
	signup_sheet = db.Boolean(default=True)