from fyg.util import confirm
from model import *

def audit():
	temps = Template.query().all()
	probs = []
	for t in temps:
		try:
			t.unrolled()
		except:
			print("unroll failed:", t.name)
			probs.append(t)
	if not probs:
		return print("you're good to go!")
	if confirm("repair %s problem templates"%(len(probs),)):
		for t in probs:
			goodsecs = []
			for s in t.sections:
				if s.get():
					goodsecs.append(s)
				else:
					print("can't find", s.urlsafe())
			t.sections = goodsecs
		if confirm("remove references to missing sections"):
			db.put_multi(probs)
			print("ok, we did it!")
	print("goodbye!")