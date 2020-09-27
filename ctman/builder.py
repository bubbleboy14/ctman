import os, datetime
from cantools.util import cmd, read, write, output
from ctman.hazards import chemicals, chemprops
from ctman.util import symage
from cantools import config

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
		data = data.replace("{{%s}}"%(i,), injects[i].replace("\n", " \\\\ "))
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

FONTFAM = """\\setmainfont[Path = fonts/%s/,
Extension=.ttf,
UprightFont=Regular,
ItalicFont=Italic,
BoldFont=Bold,
BoldItalicFont=BoldItalic]{%s}"""

def pretex(doc, fname):
	fcfg = config.ctman.font
	pname = os.path.join("build", "%s.tex"%(fname,))
	if doc.logo:
		iname = symage(doc.logo.path)
	write(read("tex/pre.tex").replace("_CLIENT_LOGO_",
		doc.logo and iname or "img/logo.jpg").replace("_SIGNUP_SHEET_",
			doc.signup_sheet and SUSHEET or "").replace("_DOC_NAME_",
			doc.name).replace("_DOC_REVISION_", str(doc.revision)).replace("_DOC_FONT_",
			fcfg.family and FONTFAM%(fcfg.family, fcfg.family) or ""), pname)
	return pname

PDINFO = {}

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
	md2pdf(mdname, bname, pname, doc)
	return bname

def initpandoc():
	if "version" not in PDINFO:
		PDINFO['version'] = int(output("pandoc --version").split("\n").pop(0).split(" ").pop().split(".").pop(0))

def md2pdf(mdname, bname, pname, doc):
	initpandoc()
	fcfg = config.ctman.font
	pcmd = "pandoc %s -o %s --%s-engine=xelatex -H tex/imps.tex -B %s -V geometry:margin=1in"%(mdname,
		bname, PDINFO['version'] == 1 and "latex" or "pdf", pname)
	if fcfg.size:
		pcmd += " -V fontsize:%s"%(fcfg.size,)
	if doc.table_of_contents:
		pcmd += " --toc -N"
	cmd(pcmd)

def build(doc):
	doc.revision += 1
	doc.put()
	afunc = doc.template and doc.template.get().content or assemble
	tempbod = afunc(doc.assembly.get("sections"))
	#fulltemp = hazard(tempbod, doc.assembly.get("hazards", {}))
	data = inject(tempbod, doc.injections)
	return export(doc, data)