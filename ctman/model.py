from cantools import db
from cantools.util import log
from ctuser.model import *
from ctedit.model import PageEdit, Style

class SecBase(db.TimeStampedBase):
	name = db.String()
	description = db.Text()
	sections = db.ForeignKey(kind="section", repeated=True)

	def secs(self, sections=None, depth=1):
		return "\r\n\r\n".join(sections and [
			db.get(s['key']).content(s['sections'], depth) for s in sections
		] or [s.content(depth=depth) for s in db.get_multi(self.sections)])

	def content(self, sections=None, depth=1):
		tline = "%s %s"%("#" * depth, self.name)
		secs = self.sections and self.secs(sections, depth + 1) or ""
		cont = "\r\n\r\n".join([tline, self.description, secs])
		log(cont)
		return cont

	def unrolled(self):
		d = self.data()
		d['sections'] = [s.unrolled() for s in db.get_multi(self.sections)]
		return d

class Section(SecBase):
	pass

class Template(SecBase):
	owner = db.ForeignKey(kind=CTUser)

class Document(db.TimeStampedBase):
	owner = db.ForeignKey(kind=CTUser)
	template = db.ForeignKey(kind=Template)
	name = db.String()
	injections = db.JSON()
	assembly = db.JSON()
	pdf = db.String()