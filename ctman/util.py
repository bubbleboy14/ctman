flags = {
	"center": {
		"start": '<p style="text-align: center;">',
		"end": "</p>",
		"tex": "\\begin{center}\r\n%s\r\n\\end{center}"
	},
	"right": {
		"start": '<p style="text-align: right;">',
		"end": "</p>",
		"tex": "\\begin{flushright}\r\n%s\r\n\\end{flushright}"
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

def trans(h, flag):
	rules = flags[flag]
	sflag = rules.get("start", "<%s>"%(flag,))
	eflag = rules.get("end", "</%s>"%(flag,))
	tex = rules["tex"]
	while sflag in h:
		start = h.index(sflag)
		end = h.index(eflag, start)
		seg = h[start + len(sflag):end]
		if "mid" in rules:
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
	for flag in flags:
		h = trans(h, flag)
	return h