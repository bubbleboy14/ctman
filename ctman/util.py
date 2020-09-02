from cantools import config

TSTART = '<table'
TSTARTEND = '<tbody>'
TEND = '\n</tr>\n</tbody>\n</table>'
TSEP = '</tr>'

swaps = {
	"<p>|": "|",
	"|</p>": "|",
	"text-align: left; ": ""
}
flags = {
	"ol": {
		"start": "<ol",
		"startend": ">",
		"liner": "1. %s"
	},
	"ul": {
		"start": "<ul",
		"startend": ">",
		"liner": "- %s"
	},
	"center": {
		"start": '<p style="text-align: center;">',
		"end": "</p>",
		"tex": "\\begin{center}\n%s\n\\end{center}"
	},
	"right": {
		"start": '<p style="text-align: right;">',
		"end": "</p>",
		"tex": "\\begin{flushright}\n%s\n\\end{flushright}"
	},
	"color": {
		"start": '<span style="color: #',
		"end": "</span>",
		"alt": {
			"split": "; background-color: #",
			"tex": "\\colorbox[HTML]{%s}{\\textcolor[HTML]{%s}{%s}}"
		},
		"mid": ';">',
		"tex": "\\textcolor[HTML]{%s}{%s}"
	},
	"background": {
		"start": '<span style="background-color: #',
		"end": "</span>",
		"alt": {
			"split": "; color: #",
			"tex": "\\textcolor[HTML]{%s}{\\colorbox[HTML]{%s}{%s}}"
		},
		"mid": ';">',
		"tex": "\\colorbox[HTML]{%s}{%s}"
	},
	"strong": {
		"tex": "\\textbf{%s}"
	},
	"em": {
		"tex": "\\emph{%s}"
	}
}

for i in range(1, 7):
	flags["h%s"%(i,)] = {
		"start": "<h%s"%(i,),
		"startend": ">",
		"tex": "#" * i + " %s"
	}

for i in range(1, 4):
	flags["t%s"%(i,)] = {
		"start": '<p style="padding-left: %spx;">'%(i * 30,),
		"end": "</p>",
		"tex": "|" + "    " * i + " %s"
	}

def clean(data):
	while "<div" in data:
		s = data.index("<div")
		se = data.index(">", s)
		e = data.index("</div>", s)
		data = data[:s] + data[se + 1 : e] + data[e + len("</div>"):]
	return data.replace("\n", "").replace("<p>", "").replace("</p>", "")

def row(chunk):
	return [clean(part.split(">", 1)[1].split("</td>")[0]) for part in chunk.split('<td')[1:]]

def table(seg):
	rowz = map(row, seg.split(TSEP))
	rowz = [rowz[0]] + [["-" * 30] * len(rowz[0])] + rowz[1:]
	return "\n".join(["| %s |"%(" | ".join(r),) for r in rowz])

flags["table"] = {
	"start": TSTART,
	"startend": TSTARTEND,
	"end": TEND,
	"handler": table
}

def trans(h, flag):
	rules = flags[flag]
	sflag = rules.get("start", "<%s>"%(flag,))
	seflag = rules.get("startend")
	eflag = rules.get("end", "</%s>"%(flag,))
	tex = rules.get("tex")
	while sflag in h:
		start = h.index(sflag)
		startend = seflag and h.index(seflag, start)
		end = h.index(eflag, start)
		seg = h[(startend or start) + len(seflag or sflag):end]
		if "handler" in rules:
			tx = rules["handler"](seg)
		elif "liner" in rules:
			lines = seg.strip().split("\n")
			mdblock = "\n".join([rules["liner"]%(s.split(">")[1].split("<")[0],) for s in lines])
			tx = "\n%s\n"%(mdblock,)
		elif "mid" in rules:
			[c, t] = seg.split(rules["mid"])
			tx = tex%(c, t)
			if "alt" in rules:
				alt = rules["alt"]
				if alt["split"] in c:
					[fg, bg] = c.split(alt["split"])
					tx = alt["tex"]%(bg, fg, t)
		else:
			tx = tex%(seg,)
		h = h[:start] + tx + h[end + len(eflag):]
	return h

lahead = [ "\\large", "\\large", "\\Large", "\\LARGE", "\\huge", "\\Huge" ]
hflags = ["%s "%("#" * i,) for i in range(1, 7)]
hflags.reverse()

def pline(line, dpref):
	for flag in hflags:
		if line.startswith(flag):
			return "%s%s"%(dpref, line)
	return line

def dhead(h, depth):
	dpref = depth * "#"
	lines = h.split("\n")
	return "\n".join(map(lambda line : pline(line, dpref), lines))

def latline(line):
	for i in range(6):
		flag = hflags[i]
		if line.startswith(flag):
			return "%s %s\n"%(lahead[i], line[len(flag):])
	return line

def lhead(h):
	return "\n".join(map(latline, h.split("\n")))

def fixhead(h, depth):
	if config.ctman.toc.secheaders:
		return dhead(h, depth)
	return lhead(h)

def h2l(h, depth=0):
	for swap in swaps:
		h = h.replace(swap, swaps[swap])
	for flag in flags:
		h = trans(h, flag)
	return fixhead(h, depth)