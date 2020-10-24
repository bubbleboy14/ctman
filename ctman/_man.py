from cantools.web import respond, succeed, cgi_get
from ctman.builder import build, export
from model import db

def response():
	entity = db.get(cgi_get("key"))
	if entity.polytype == "document":
		entity.pdf = build(entity)
		entity.put()
		succeed(entity.data())
	else: # build fragment
		succeed(export(entity))

respond(response)