import os, datetime
from cantools.util import cmd, read, write, sym
from ctman.hazards import chemicals, chemprops

def part(fname):
	return "# %s\r\n%s"%(fname.split(".")[0], read(os.path.join("templates", fname)))

def assemble(sections): # do something w/ sections[]
	for dirpath, dirnames, filenames in os.walk("templates"):
		return "\n\n".join([part(fname) for fname in filenames])

def hazard(template, arules): # do non-chems as well
	chems = arules.get("chemical")
	if not chems: return template
	chart = [chemprops, ["-"*((i+1)*5) for i in range(len(chemprops))]]
	for chem in chems:
		chart.append([chemicals[chem][p] for p in chemprops])
	return "%s\r\n\r\n# Hazards - Chemical\r\n\r\n| %s |"%(template,
		" |\r\n| ".join(map(lambda r : " | ".join(r), chart)))

def inject(data, injects):
	for i in injects:
		data = data.replace("{%s}"%(i,), injects[i])
	return data

SUSHEET = """\\begin{center}
{\\huge Sign-in Sheet}
\\begin{tabular}{ |p{2.5cm}|p{2.5cm}|p{2.5cm}|p{2.5cm}| }
\\hline
Name & Signature & Company & Date \\\\ \\hline
%s \\\\ \\hline
\\end{tabular}
\\end{center}
"""%("\\\\ \\hline\r\n".join([" & & & " for i in range(40)]),)

def pretex(doc, fname):
	pname = os.path.join("build", "%s.tex"%(fname,))
	if doc.logo:
		iname = os.path.join("build", "%s.jpg"%(doc.logo.value,))
		if not os.path.exists(iname):
			sym("../%s"%(doc.logo.path,), iname)
	write(read("tex/pre.tex").replace("_CLIENT_LOGO_",
		doc.logo and iname or "img/logo.jpg").replace("_SIGNUP_SHEET_",
			SUSHEET), pname)
	return pname

def export(doc, data):
	fname = "_".join(str(datetime.datetime.now()).split(".")[0].split(" "))
	mdname = os.path.join("build", "%s.md"%(fname,))
	write("\\newpage%s"%(data,), mdname)
	bname = os.path.join("build", "%s.pdf"%(fname,))
	pname = pretex(doc, fname)
	cmd("pandoc %s -o %s --toc -H tex/imps.tex -B %s"%(mdname, bname, pname))
	return bname

def build(doc):
	afunc = doc.template and doc.template.get().content or assemble
	tempbod = afunc(doc.assembly.get("sections"))
	fulltemp = hazard(tempbod, doc.assembly.get("hazards", {}))
	data = inject(fulltemp, doc.injections)
	return export(doc, data)