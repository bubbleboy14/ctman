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
		"liner": "1. %s"
	},
	"ul": {
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
	flags["h%s"%(i,)] = { "tex": "#" * i + " %s" }

for i in range(1, 4):
	flags["t%s"%(i,)] = {
		"start": '<p style="padding-left: %spx;">'%(i * 30,),
		"end": "</p>",
		"tex": "|" + "    " * i + " %s"
	}

def row(chunk):
	return [part.split("<")[0] for part in chunk.split('">')[2:]]

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
			lines = seg[1:-1].split("\n")
			mdblock = "\n".join([rules["liner"]%(s[4:-5],) for s in lines])
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

def h2l(h):
	for swap in swaps:
		h = h.replace(swap, swaps[swap])
	for flag in flags:
		h = trans(h, flag)
	return h