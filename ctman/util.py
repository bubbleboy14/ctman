flags = {
	"color:": {
		"start": '<span style="color: #',
		"end": "</span>",
		"mid": ';">',
		"tex": "\\textcolor[HTML]{%s}{%s}"
	},
	"strong": {
		"tex": "\\textbf{%s}"
	},
	"em": {
		"tex": "\\emph{%s}"
	}
}

def h2l(h):
	for flag in flags:
		rules = flags[flag]
		sflag = rules.get("start", "<%s>"%(flag,))
		eflag = rules.get("end", "</%s>"%(flag,))
		tex = rules["tex"]
		while sflag in h:
			start = h.index(sflag)
			end = h.index(eflag)
			seg = h[start + len(sflag):end]
			if "mid" in rules:
				[c, t] = seg.split(rules["mid"])
				h = h[:start] + tex%(c, t) + h[end + len(eflag):]
			else:
				h = h[:start] + tex%(seg,) + h[end + len(eflag):]
	return h