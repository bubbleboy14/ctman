import os, datetime, magic
from cantools.util import cmd, read, write, sym
from ctman.hazards import chemicals, chemprops

def part(fname):
	return "# %s\n%s"%(fname.split(".")[0], read(os.path.join("templates", fname)))

def assemble(sections): # do something w/ sections[]
	for dirpath, dirnames, filenames in os.walk("templates"):
		return "\n\n".join([part(fname) for fname in filenames])

def hazard(template, arules): # do non-chems as well
	chems = arules.get("chemical")
	if not chems: return template
	chart = [chemprops, ["---"*((i+1)*5) for i in range(len(chemprops))]]
	for chem in chems:
		chart.append([chemicals[chem][p] for p in chemprops])
	return "%s\n\n# Hazards - Chemical\n\n| %s |"%(template,
		" |\n| ".join(map(lambda r : " | ".join(r), chart)))

def inject(data, injects):
	for i in injects:
		data = data.replace("{{%s}}"%(i,), injects[i].replace("\n\n", "\\\n"))
	return data

SUSHEET = """\\newpage
\\begin{center}
{\\huge Sign-in Sheet}
\\begin{tabular}{ |p{3cm}|p{3cm}|p{3cm}|p{3cm}| }
\\hline
Name & Signature & Company & Date \\\\ \\hline
%s \\\\ \\hline
\\end{tabular}
\\end{center}
"""%("\\\\ \\hline\r\n".join([" & & & " for i in range(40)]),)

def pretex(doc, fname):
	pname = os.path.join("build", "%s.tex"%(fname,))
	if doc.logo:
		iname = os.path.join("build", "%s.%s"%(doc.logo.value,
			magic.from_file(doc.logo.path).split(" ").pop(0).lower()))
		if not os.path.exists(iname):
			sym("../%s"%(doc.logo.path,), iname)
	write(read("tex/pre.tex").replace("_CLIENT_LOGO_",
		doc.logo and iname or "img/logo.jpg").replace("_SIGNUP_SHEET_",
			doc.signup_sheet and SUSHEET or "").replace("_DOC_NAME_",
			doc.name).replace("_DOC_REVISION_", str(doc.revision)), pname)
	return pname

def export(doc, data):
	if doc.pretty_filenames:
		fname = "%s_r%s"%(doc.name.replace(" ", "_").replace("(",
			"").replace(")", ""), doc.revision)
	else:
		fname = "_".join(str(datetime.datetime.now()).split(".")[0].split(" "))
	mdname = os.path.join("build", "%s.md"%(fname,))
	write("\\newpage\n%s"%(data,), mdname)
	bname = os.path.join("build", "%s.pdf"%(fname,))
	pname = pretex(doc, fname)
	pcmd = "pandoc %s -o %s -H tex/imps.tex -B %s -V geometry:margin=1in"%(mdname, bname, pname)
	if doc.table_of_contents:
		pcmd += " --toc -N"
	cmd(pcmd)
	return bname

def build(doc):
	doc.revision += 1
	doc.put()
	afunc = doc.template and doc.template.get().content or assemble
	tempbod = afunc(doc.assembly.get("sections"))
	fulltemp = hazard(tempbod, doc.assembly.get("hazards", {}))
	data = inject(fulltemp, doc.injections)
	return export(doc, data)