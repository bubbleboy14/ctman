from datetime import datetime, timedelta
from cantools.web import respond, send_email
from cantools.util import log
from model import *

EMSG = """your subscription has %s expired.

please renew your subscription on the account page."""

def response():
	today = datetime.now()
	tomorrow = today + timedelta(1)
	yesterday = today - timedelta(1)
	mems = Member.query().all()
	log("memscan! found %s members"%(len(mems),))
	unregistered = []
	expired = []
	almost = []
	for mem in mems:
		ex = mem.expiration
		if not ex:
			unregistered.append(mem)
		elif ex > yesterday:
			if ex < today:
				expired.append(mem)
			elif ex < tomorrow:
				almost.append(mem)
	log("%s unregistered"%(len(unregistered),))
	log("%s expired"%(len(expired),))
	log("%s almost exired"%(len(almost),))
	for mem in expired:
		send_email(to=mem.email, subject="your subscription",
			body=EMSG%("just",))
	for mem in almost:
		send_email(to=mem.email, subject="your subscription",
			body=EMSG%("almost",))
	log("goodbye")

respond(response)