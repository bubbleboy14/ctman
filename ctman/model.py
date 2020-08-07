from cantools import db
from ctuser.model import *
from ctedit.model import PageEdit, Style

class Section(db.TimeStampedBase):
	name = db.String()
	description = db.Text()
	sections = db.ForeignKey(kind="section", repeated=True)

class Template(Section):
	pass

class Document(db.TimeStampedBase):
	owner = db.ForeignKey(kind=CTUser)
	template = db.ForeignKey(kind=Template)
	name = db.String()
	injections = db.JSON()
	assembly = db.JSON()
	pdf = db.String()