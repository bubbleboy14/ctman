from cantools.web import respond, succeed, cgi_get
from ctman.builder import build, export
from model import db

def response():
	entity = db.get(cgi_get("key"))
	if entity.polytype == "document":
		bdata = build(entity)
		if bdata["success"]:
			entity.revision += 1
			entity.pdf = bdata["build"]
			entity.put()
		succeed({
			"build": bdata,
			"doc": entity.data()
		})
	else: # build fragment
		succeed(export(entity))

respond(response)