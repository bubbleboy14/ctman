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