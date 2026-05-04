import os, datetime, shutil
from condox.util import symage, colormap
from ctman.hazards import chemicals, chemprops
from cantools.util import read, write, output
from cantools.web import mail
from cantools import config
from model import db, Injection

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

def inject(data, injects=None):
	if not injects: # preview mode
		print("extracting injection variables from fragment")
		possibles = [b.split("}}")[0] for b in data.split("{{")]
		print("examining %s injection variable candidates"%(len(possibles),))
		injects = {}
		for name in possibles:
			injection = Injection.query(Injection.name == name).get()
			if injection:
				print(name)
				injects[name] = injection.fallback or "undefined"
		print("using fallbacks for %s injection variables"%(len(injects.keys()),))
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

\\setmathfont{latinmodern-math.otf}"""

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

def pretex(doc, fname, styleonly=False):
	fcfg = config.ctman.font
	pname = os.path.join("build", "%s.tex"%(fname,))
	if not styleonly and doc.logo:
		iname = symage(doc.logo.path)
	ff = getattr(doc, "font", None) or fcfg.family
	fontdesc = ff and FONTFAM%(ff, ff) or ""
	colors = colormap.definitions()
	write(styleonly and "%s\n%s"%(fontdesc, colors) or read("tex/pre.tex").replace("_CLIENT_LOGO_",
		doc.logo and iname or "img/logo.jpg").replace("_DECLARATION_PAGE_",
			doc.declaration_page and dex(doc) or "").replace("_SIGNUP_SHEET_",
			doc.signup_sheet and SUSHEET or "").replace("_DOC_NAME_",
			doc.name).replace("_DOC_REVISION_",
			str(doc.revision)).replace("_DOC_FONT_",
			fontdesc).replace("_DOC_COLORS_", colors), pname)
	return pname

PDINFO = {}

def report(bdata):
	mail.email_reportees("uh oh!", "\n".join([
		"path: " + bdata["build"],
		"success: " + str(bdata["success"]),
		"message:",
		bdata["message"]
	]))

def matching_brace(data, open_index):
	depth = 0
	for i in range(open_index, len(data)):
		if data[i] == "\\":
			continue
		if data[i] == "{" and (i == 0 or data[i - 1] != "\\"):
			depth += 1
		elif data[i] == "}" and (i == 0 or data[i - 1] != "\\"):
			depth -= 1
			if depth == 0:
				return i
	return -1

def strip_table_highlights(data):
	lines = data.splitlines(True)
	filtered = []
	i = 0
	while i < len(lines):
		line = lines[i]
		if line.lstrip().startswith("\\sethlcolor") and "\\hl{" in line:
			j = i + 1
			while j < len(lines) and not lines[j].strip():
				j += 1
			if j < len(lines) and lines[j].lstrip().startswith("\\begin{tabular}"):
				i += 1
				continue
		filtered.append(line)
		i += 1
	data = "".join(filtered)

	hlcolor = "\\sethlcolor"
	out = []
	pos = 0
	while True:
		start = data.find(hlcolor, pos)
		if start == -1:
			out.append(data[pos:])
			return "".join(out)
		out.append(data[pos:start])
		color_start = start + len(hlcolor)
		if color_start >= len(data) or data[color_start] != "{":
			out.append(data[start:start + len(hlcolor)])
			pos = start + len(hlcolor)
			continue
		color_end = matching_brace(data, color_start)
		if color_end == -1:
			out.append(data[start:])
			return "".join(out)
		hl_start = color_end + 1
		while hl_start < len(data) and data[hl_start].isspace():
			hl_start += 1
		if not data.startswith("\\hl{", hl_start):
			out.append(data[start:color_end + 1])
			pos = color_end + 1
			continue
		body_start = hl_start + len("\\hl")
		body_end = matching_brace(data, body_start)
		if body_end == -1:
			out.append(data[start:])
			return "".join(out)
		out.append(data[body_start + 1:body_end])
		pos = body_end + 1

def escape_percent(data):
	out = []
	for i, char in enumerate(data):
		out.append("\\%" if char == "%" and (i == 0 or data[i - 1] != "\\") else char)
	return "".join(out)

def row_columns(line):
	return 1 + sum(1 for i, char in enumerate(line) if char == "&" and (i == 0 or line[i - 1] != "\\"))

def normalize_tabular_columns(data):
	lines = data.splitlines(True)
	out = []
	i = 0
	while i < len(lines):
		line = lines[i]
		if not line.lstrip().startswith("\\begin{tabular}{"):
			out.append(line)
			i += 1
			continue
		block = [line]
		i += 1
		while i < len(lines):
			block.append(lines[i])
			i += 1
			if lines[i - 1].lstrip().startswith("\\end{tabular}"):
				break
		declared = block[0].count("p{")
		actual = max([row_columns(row) for row in block[1:] if "\\\\" in row] or [declared])
		if declared == 1 and actual > declared:
			width = str(1.0 / actual)[:4]
			block[0] = "\\begin{tabular}{| %s |}\n"%(" | ".join(actual * ["p{%s\\linewidth}"%(width,)]),)
		out.extend(block)
	return "".join(out)

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
			data = doc.content(depth=1)#, novars=True)
			data = inject(data)
			pname = pretex(doc, fname, True)
		except Exception as e:
			return {
				"message": str(e),
				"success": False
			}
	data = escape_percent(normalize_tabular_columns(strip_table_highlights(data)))

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

def xelatex():
	return shutil.which("xelatex") or (os.path.exists("/Library/TeX/texbin/xelatex") and "/Library/TeX/texbin/xelatex") or "xelatex"

def md2pdf(doc, mdname, bname, pname=None):
	initpandoc()
	mcfg = config.ctman
	fcfg = mcfg.font
	pcmd = "pandoc %s -o %s --%s-engine=%s -H tex/imps.tex -V geometry:margin=0.8in"%(mdname,
		bname, PDINFO['version'] == 1 and "latex" or "pdf", xelatex())
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
	for injection in db.get_multi(doc.template.get().injections):
		if injection.name not in injectz:
			injectz[injection.name] = injection.fallback or "undefined"
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
