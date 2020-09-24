import os, magic
from cantools import config
from cantools.util import sym, cmd, log

TSTART = '<table'
TSTARTEND = '<tbody>'
TEND = '\n</tr>\n</tbody>\n</table>'
TSEP = '</tr>'

swaps = {
	"_": "\\_",
	"<p>|": "|",
	"|</p>": "|",
	"&ndash;": "-",
	"<br />": "\\hfill\\break\\hfill\\break ",
	"&amp;": "\\&",
	"&ldquo;": '"',
	"&rdquo;": '"',
	"&bull;": "\\textbullet",
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
	"underline": {
		"start": '<span style="text-decoration: underline;">',
		"end": "</span>",
		"tex": "\\underline{%s}"
	},
	"u": {
		"tex": "\\underline{%s}"
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
	},
	"p": {
		"tex": "%s"
	},
	"a": {
		"start": "<a",
		"startend": ">",
		"tex": "%s"
	},
	"img": {
		"start": '<img style="display: block; max-width: 100%;" src="../',
		"endstart": '" ',
		"end": ' />',
		"tex": "\\includegraphics[width=\\linewidth]{%s}"
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
	data = data.replace("\n", "")
	if "<p" in data:
		return "\\Centerstack{%s}"%(trans(trans(data, "p"), "p", {
			"start": "<p",
			"startend": ">",
			"tex": " \\\\ %s"
		}),)
	return data

def row(chunk):
	return [clean(part.split(">", 1)[1].split("</td>")[0]) for part in chunk.split('<td')[1:]]

TBL = """\\begin{center}
\\begin{tabular}{%s}
%s
\\end{tabular}
\\end{center}"""

def table(seg):
	rowz = map(row, seg.split(TSEP))
	numcols = len(rowz[0])
	if "img" in seg:
		iorig = flags["img"]
		seg = trans(seg, "img", {
			"start": iorig["start"],
			"endstart": iorig["endstart"],
			"end": iorig["end"],
			"tex": "\\includegraphics[width=" + str(1.0 / numcols)[:3] + "\\linewidth]{%s}"
		})
		rowz = map(row, seg.split(TSEP))
		return TBL%(numcols * "c", "\\\\\n\n".join([" & ".join(r) for r in rowz]))
	else:
		rowz = [rowz[0]] + [["-" * 30] * numcols] + rowz[1:]
		return "\n".join(["| %s |"%(" | ".join(r),) for r in rowz])

TABLE_FLAGS = {
	"start": TSTART,
	"startend": TSTARTEND,
	"end": TEND,
	"handler": table
}

def symage(path):
	ext = magic.from_file(path).split(" ").pop(0).lower()
	if ext not in ["png", "jpeg"]:
		log("converting %s to png!"%(ext,))
		cmd("convert -append -alpha off %s %s.png"%(path, path))
		cmd("mv %s.png %s"%(path, path))
		ext = "png"
	sname = "%s.%s"%(path.replace("blob", "build"), ext)
	if not os.path.exists(sname):
		sym("../%s"%(path,), sname)
	return sname

def trans(h, flag, rules=None):
	rules = rules or flags[flag]
	sflag = rules.get("start", "<%s>"%(flag,))
	seflag = rules.get("startend")
	esflag = rules.get("endstart")
	eflag = rules.get("end", "</%s>"%(flag,))
	tex = rules.get("tex")
	while sflag in h:
		start = h.index(sflag)
		startend = seflag and h.index(seflag, start)
		startender = (startend or start) + len(seflag or sflag)
		endstart = esflag and h.index(esflag, startender)
		end = h.index(eflag, startender or start)
		seg = h[startender : (endstart or end)]
		if "handler" in rules:
			tx = rules["handler"](seg)
		elif "liner" in rules:
			lines = seg.strip().split("</li>")[:-1]
			mdblock = "\n".join([rules["liner"]%(s.split(">")[1],) for s in lines])
			tx = "\n%s\n"%(mdblock,)
		elif "mid" in rules:
			[c, t] = seg.split(rules["mid"], 1)
			tx = tex%(c, t)
			if "alt" in rules:
				alt = rules["alt"]
				if alt["split"] in c:
					[fg, bg] = c.split(alt["split"])
					tx = alt["tex"]%(bg, fg, t)
		else:
			if flag == "img":
				seg = symage(seg)
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
			return "%s{%s}\\normalsize"%(lahead[i], line[len(flag):])
	return line

def lhead(h):
	return "\n".join(map(latline, h.split("\n")))

def fixhead(h, depth):
	if not (config.ctman and config.ctman.toc.secheaders):
		return lhead(h)
	return dhead(h, depth)

def h2l(h, depth=0):
	for swap in swaps:
		h = h.replace(swap, swaps[swap])
	h = trans(h, "table", TABLE_FLAGS)
	for flag in flags:
		h = trans(h, flag)
	return fixhead(h, depth)