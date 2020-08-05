from cantools import db
from ctuser.model import *
from ctedit.model import PageEdit, Style

class Document(db.TimeStampedBase):
	owner = db.ForeignKey(kind=CTUser)
	name = db.String()
	injections = db.JSON()
	assembly = db.JSON()
	pdf = db.String()