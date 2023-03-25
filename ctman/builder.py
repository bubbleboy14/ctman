import os, datetime
from cantools.util import read, write, output
from ctman.hazards import chemicals, chemprops
from ctman.util import symage
from cantools.web import mail
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
		" |\n| ".join([" | ".join(r) for r in chart]))

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
BoldItalicFont=BoldItalic]{%s}

\\setmathfont{Latin Modern Math}"""

DEX = """\\newpage
SITE-SPECIFIC HEALTH AND SAFETY PLAN
\\begin{flushright}(HASP)\\end{flushright}

\\begin{tabular}{ p{6cm} p{6cm} }
%s
\\end{tabular}
"""

def drow(k, v):
	return "%s: & %s \\\\ \\\\"%(k, v.replace("\n", "\\hfill\\break"))

def tsrow(k, v):
	return drow(k, v.strftime("%B %d, %Y"))

def dex(doc):
	rows = []
	for k, v in list(doc.declarations.items()):
		rows.append(drow(k, v))
	rows.append(tsrow("DATE PREPARED", doc.created))
	rows.append(tsrow("DATE REVISED", doc.modified))
	rows.append(tsrow("DATE EXPIRES",
		datetime.datetime(doc.modified.year + 1,
		doc.modified.month, doc.modified.day)))
	return DEX%("\n".join(rows),)

def pretex(doc, fname, fontonly=False):
	fcfg = config.ctman.font
	pname = os.path.join("build", "%s.tex"%(fname,))
	if not fontonly and doc.logo:
		iname = symage(doc.logo.path)
	ff = getattr(doc, "font", None) or fcfg.family
	fontdesc = ff and FONTFAM%(ff, ff) or ""
	write(fontonly and fontdesc or read("tex/pre.tex").replace("_CLIENT_LOGO_",
		doc.logo and iname or "img/logo.jpg").replace("_DECLARATION_PAGE_",
			doc.declaration_page and dex(doc) or "").replace("_SIGNUP_SHEET_",
			doc.signup_sheet and SUSHEET or "").replace("_DOC_NAME_",
			doc.name).replace("_DOC_REVISION_",
			str(doc.revision)).replace("_DOC_FONT_", fontdesc), pname)
	return pname

PDINFO = {}

def report(bdata):
	mail.email_reportees("uh oh!", "\n".join([
		"path: " + bdata["build"],
		"success: " + str(bdata["success"]),
		"message:",
		bdata["message"]
	]))

def export(doc, data=None):
	fname = doc.name.replace(" ", "_").replace("(",
		"").replace(")", "").replace("/", "")
	if doc.polytype == "document":
		if doc.pretty_filenames:
			fname = "%s_r%s"%(fname, doc.revision)
		else:
			fname = "_".join(str(datetime.datetime.now()).split(".")[0].split(" "))
		data = "\\newpage\n%s"%(data,)
		pname = pretex(doc, fname)
	else:
		try:
			data = doc.content(depth=1, novars=True)
			pname = pretex(doc, fname, True)
		except Exception as e:
			return {
				"message": str(e),
				"success": False
			}

	mdname = os.path.join("build", "%s.md"%(fname,))
	write(data, mdname)
	bname = os.path.join("build", "%s.pdf"%(fname,))
	panout = md2pdf(doc, mdname, bname, pname)
	bdata = {
		"build": bname,
		"message": panout,
		"success": "Error producing PDF" not in panout
	}
	panout and report(bdata)
	return bdata

def initpandoc():
	if "version" not in PDINFO:
		PDINFO['version'] = int(output("pandoc --version").split("\n").pop(0).split(" ").pop().split(".").pop(0))

def md2pdf(doc, mdname, bname, pname=None):
	initpandoc()
	mcfg = config.ctman
	fcfg = mcfg.font
	pcmd = "pandoc %s -o %s --%s-engine=xelatex -H tex/imps.tex -V geometry:margin=0.8in"%(mdname,
		bname, PDINFO['version'] == 1 and "latex" or "pdf")
	if mcfg.builder.verbose:
		pcmd = "%s --verbose"%(pcmd,)
	if fcfg.size:
		pcmd += " -V fontsize:%s"%(fcfg.size,)
	if pname:
		pcmd += " -B %s"%(pname,)
	if doc.polytype == "document" and doc.table_of_contents:
		pcmd += " --toc -N"
	return output(pcmd)

def injectedDoc(tempbod, doc):
	injectz = doc.injections.copy()
	if config.ctman.builder.injeclarations:
		injectz.update(doc.declarations)
	return inject(tempbod, injectz)

def build(doc):
	try:
		afunc = doc.template and doc.content or assemble
		tempbod = afunc(doc.assembly.get("sections"))
		#fulltemp = hazard(tempbod, doc.assembly.get("hazards", {}))
		data = injectedDoc(tempbod, doc)
		return export(doc, data)
	except Exception as e:
		return {
			"message": str(e),
			"success": False
		}