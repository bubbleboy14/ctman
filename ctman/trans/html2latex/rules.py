# -*- coding: UTF-8 -*-

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
		"tex": "\\includegraphics[width=\\linewidth]{%s}",
		"sym": True
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