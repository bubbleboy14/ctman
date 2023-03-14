from cantools.web import respond, succeed, cgi_get
from ctman.builder import build, export
from model import db

def response():
	action = cgi_get("action", default="build", choices=["build", "embedders"])
	entity = db.get(cgi_get("key"))
	if action == "embedders":
		succeed([e.data() for e in entity.embedders()])
	elif entity.polytype == "document":
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