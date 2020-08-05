from cantools.web import respond, succeed, cgi_get
from builder import build
from model import db

def response():
	doc = db.get(cgi_get("key"))
	doc.pdf = build(doc.injections, doc.assembly)
	doc.put()
	succeed(doc.data())

respond(response)