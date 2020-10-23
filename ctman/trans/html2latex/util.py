# -*- coding: UTF-8 -*-

import os, magic
from cantools.util import sym, cmd, log

headers = {
	"latex": [ "\\large", "\\large", "\\Large", "\\LARGE", "\\huge", "\\Huge" ],
	"section": ["%s "%("#" * i,) for i in range(1, 7)]
}
headers["section"].reverse()

# maybe rm some swaps???
swaps = {
	"_": "\\_",
	"<p>|": "|",
	"|</p>": "|",
	"&sect;": "§",
	"&ndash;": "-",
	"<br />": " \\hfill\\break ",
	"&amp;": "\\&",
	"&mu;": "$\\mu$",
	"&ldquo;": '"',
	"&rdquo;": '"',
	"&bull;": "\\textbullet",
	"text-align: left; ": "",
	"padding-left: 60px; text-align: center;": "text-align: center;",
	'<span style="text-align: center; ': '<span style="'
}

flags = {
	"p": {
		"tex": "\\hfill\\break %s \\hfill\\break"
	},
	"div": {
		"tex": "\\hfill\\break %s \\hfill\\break"
	},
	"span": {
		"tex": " %s "
	},
	"a": {
		"tex": " %s "
	},
	"strong": {
		"tex": "\\textbf{%s}"
	},
	"em": {
		"tex": "\\emph{%s}"
	},
	"u": {
		"tex": "\\underline{%s}"
	},
	"img": {
		"start": '<img style="display: block; max-width: 100%;" src="../',
		"endstart": '" ',
		"end": ' />',
		"tex": "\\includegraphics[width=\\linewidth]{%s}"
	},
	"ol": {
		"liner": "1. %s"
	},
	"ul": {
		"liner": "- %s"
	}
}

tflags = {
	"p": {
		"tex": " \\\\ %s \\\\ "
	},
	"div": {
		"tex": " \\\\ %s \\\\ "
	}
}

for i in range(1, 7):
	flags["h%s"%(i,)] = {
		"tex": "#" * i + " %s"
	}
	tflags["h%s"%(i,)] = {
		"tex": headers["latex"][6 - i] + "{%s}\\normalsize "
	}

styles = {
	"text-align": {
		"center": "\\begin{center}\n%s\n\\end{center}",
		"right": "\\begin{flushright}\n%s\n\\end{flushright}",
		"left": "\\begin{flushleft}\n%s\n\\end{flushleft}"
	},
	"text-decoration": {
		"underline": "\\underline{%s}"
	},
	"padding-left": {}
}

for i in range(1, 4):
	styles["padding-left"]["%spx"%(i * 30,)] = "\\begin{addmargin}[" + str(i) + "cm]{0cm}\n%s\n\\end{addmargin}"

cstyles = {
	"background-color": "\\colorbox[HTML]{%s}{%s}",
	"color": "\\textcolor[HTML]{%s}{%s}"
}

#
# misc
#

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

def getstart(h, sflag):
	i = h.find(sflag)
	while h.find(sflag, i + 1) != -1:
		i = h.find(sflag, i + 1)
	return i

def nextlast(h, flagz):
	f = None
	i = 0
	for flag in flagz:
		sflag = flagz[flag].get("start", "<%s"%(flag,))
		fi = getstart(h, sflag)
		if fi > i:
			i = fi
			f = flag
	return f

def trans(h, flag, rules=None):
	rules = rules or flags[flag]
	sflag = rules.get("start", "<%s"%(flag,))
	seflag = rules.get("startend", ">")
	esflag = rules.get("endstart")
	eflag = rules.get("end", "</%s>"%(flag,))
	tex = rules.get("tex")
	while sflag in h:
		start = getstart(h, sflag)
		startend = h.index(seflag, start)
		startender = (startend or start) + len(seflag or sflag)
		endstart = esflag and h.index(esflag, startender)
		end = h.index(eflag, startender or start)
		seg = h[startender : (endstart or end)]
		if "handler" in rules:
			tx = rules["handler"](seg)
		elif "liner" in rules:
			lines = seg.strip().split("</li>")
			epart = lines.pop().replace("-", "    -")
			mdblock = "\n".join([rules["liner"]%(s.split(">", 1)[1],) for s in lines])
			tx = "\n%s\n%s\n"%(mdblock, epart)
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

#
# tables
#

TBL = """\\begin{center}
\\begin{tabular}{%s}
%s
\\end{tabular}
\\end{center}"""

def clean(data):
	data = data.replace("\n", " ")
	if "<" in data:
		for flag in tflags:
			data = trans(data, flag, tflags[flag])
		data = "\\Centerstack{%s}"%(data,)
	return data

def row(chunk):
	return [clean(part.split(">", 1)[1].split("</td>")[0]) for part in chunk.split('<td')[1:]]

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
		return "\n".join(map(bartable, rowsets(rowz)))

TABLE_FLAGS = {
	"startend": '<tbody>',
	"end": '\n</tr>\n</tbody>\n</table>',
	"handler": table
}

def rowsets(rows):
	sets = []
	curnum = None
	while len(rows):
		item = rows.pop(0)
		if curnum != len(item):
			curnum = len(item)
			if curnum == 1:
				curset = []
			else:
				curset = [["   "] * curnum]
			sets.append(curset)
		curset.append(item)
	if len(sets) == 1:
		sets[0].pop(0)
	return sets

def bartable(rowz):
	if not rowz:
		return ""
	numcols = len(rowz[0])
	if numcols == 1 and len(rowz) == 1:
		return "\\begin{center}\n%s\n\\end{center}"%(rowz[0][0],)
	rowz = [rowz[0]] + [["-" * 30] * numcols] + rowz[1:]
	return "\n%s"%("\n".join(["| %s |"%(" | ".join(r),) for r in rowz]),)