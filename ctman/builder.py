import os, datetime
from cantools.util import cmd, read, write
from ctman.hazards import chemicals, chemprops

def part(fname):
	return "# %s\r\n%s"%(fname.split(".")[0], read(os.path.join("templates", fname)))

def assemble(arules): # do something w/ arules{...}
	for dirpath, dirnames, filenames in os.walk("templates"):
		return "\n\n".join([part(fname) for fname in filenames])

def hazard(template, arules): # do non-chems as well
	chems = arules.get("hazards", { "chemical": [] })["chemical"]
	if not chems: return template
	chart = [chemprops, ["---" for p in chemprops]]
	for chem in chems:
		chart.append([chemicals[chem][p] for p in chemprops])
	return "%s\r\n\r\n# Hazards - Chemical\r\n\r\n%s"%(template,
		"\r\n".join(map(lambda r : " | ".join(r), chart)))

def inject(data, injects):
	for i in injects:
		data = data.replace("{%s}"%(i,), injects[i])
	return data

def export(data):
	fname = "_".join(str(datetime.datetime.now()).split(".")[0].split(" "))
	mdname = os.path.join("build", "%s.md"%(fname,))
	write(data, mdname)
	bname = os.path.join("build", "%s.pdf"%(fname,))
	cmd("pandoc %s -o %s --toc -H tex/imps.tex -B tex/pre.tex"%(mdname, bname))
	return bname

def build(injects, assembly):
	template = assemble(assembly)
	fulltemp = hazard(template, assembly)
	data = inject(fulltemp, injects)
	return export(data)