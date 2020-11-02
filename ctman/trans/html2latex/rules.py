# -*- coding: UTF-8 -*-

headers = {
	"latex": [ "\\large", "\\large", "\\Large", "\\LARGE", "\\huge", "\\Huge" ],
	"section": ["%s "%("#" * i,) for i in range(1, 7)]
}
headers["section"].reverse()

# maybe rm some swaps???
swaps = {
	# basics:
	"&amp;": "\\&",
	"&mu;": "$\\mu$",
	"&shy;": "\\-",
	"&cent;": "\\textcent"
	"&euro;": "\\texteuro",
	"&pound;": "\\textsterling",
	"&yen;": "\\textyen",
	"&copy;": "\\textcopyright",
	"&reg;": "\\textregistered",
	"&trade;": "\\texttrademark",
	"&permil;": "\\textperthousand",
	"&micro;": "$\\mu$",
	"&middot;": "\\textbullet",
	"&bull;": "\\textbullet",
	"&hellip;": "\\ldots",
	"&prime;": "$\\prime$",
	"&Prime;": "$\\prime\\prime$",
	"&sect;": "§",
	"&para;": "\\textparagraph",
	"&szlig;": "\\ss",
	"&lsaquo;": "\\guilsinglleft",
	"&rsaquo;": "\\guilsinglright",
	"&laquo;": "\\guillemotleft",
	"&lsquo;": "`",
	"&rsquo;": "'",
	"&ldquo;": "\\textquotedblleft",
	"&rdquo;": "\\textquotedblright",
	"&sbquo;": ",",
	"&bdquo;": ",,",
	"&lt;": "\\textless",
	"&gt;": "\\textgreater",
	"&le;": "\\leq",
	"&ge;": "\\geq",
	"&ndash;": "\\textendash",
	"&mdash;": "\\textemdash",
	"&macr;": "\\textasciimacron",
	"&oline;"
	"&curren;": "\\textcurrency",
	"&brvbar;": "\\textbrokenbar",
	"&uml;": "\\textasciidieresis",
	"&iexcl;": "\\textexclamdown",
	"&iquest;": "\\textquestiondown",
	"&circ;": "\\circ",
	"&tilde;": "\\texttildelow",
	"&deg;": "\\textdegree",
	"&minus;": "-",
	"&plusmn;": "$\\pm$",
	"&divide;": "$\\div$",
	"&frasl;": "/",

	"&times;": "\\texttimes",
	"&sup1;": "$^1$",
	"&sup2;": "$^2$",
	"&sup3;": "$^3$",
	"&frac14;": "\\textonequarter",
	"&frac12;": "\\textonehalf",
	"&frac34;": "\\textthreequarters"
	"&fnof;": "$f$",
	"&int;": "\\int_{}^{}",
	"&sum;": "\\Sigma",
	"&infin;": "\\infty",
	"&radic;": "\\sqrt",
	"&sim;": "\\sim",
	"&cong;": "\\cong",
	"&asymp;": "\\approx",
	"&ne;": "\\neq",
	"&equiv;": "\\equiv",
	"&isin;": "\\in",
	"&notin;": "\\notin",
	"&ni;": "\\ni",
	"&prod;": "\\prod",
	"&and;": "\\land",
	"&or;": "\\lor",
	"&not;": "\\neg",
	"&cap;": "\\cap",

	"&cup;": "\\cup",
	"&part;": "\\partial",
	"&forall;": "\\forall",
	"&exist;": "\\exists",
	"&empty;", "\\varnothing",
	"&nabla;": "\\nabla",
	"&lowast;": "\\ast",
	"&prop;": "\\propto",
	"&ang;": "\\angle",
	"&acute;": "\\textasciiacute",
	"&cedil;": "\\c{}",
	"&ordf;": "\\textordfeminine",
	"&ordm;": "\\textordmasculine",
	"&dagger;": "\\textdagger",
	"&Dagger;": "\\textdaggerdbl",
	"&Agrave;": "\\`{A}",
	"&Aacute;": "\\'{A}",
	"&Acirc;": "\\^{A}",
	"&Atilde;": "\\~{A}",
	"&Auml;": '\\"{A}',
	"&Aring;": "\\AA{}",
	"&AElig;": "\\AE{}",
	"&Ccedil;": "\\c{C}",
	"&Egrave;": "\\`{E}",

	"&Eacute;": "\\'{E}",
	"&Ecirc;": "\\^{E}",
	"&Euml;": '\\"{E}',
	"&Igrave;": "\\`{I}",
	"&Iacute;": "\\'{I}",
	"&Icirc;": "\\^{I}",
	"&Iuml;": '\\"{I}',
	"&ETH;": "\\DH{}",
	"&Ntilde;": "\\~{N}",
	"&Ograve;": "\\`{O}",
	"&Oacute;": "\\'{O}",
	"&Ocirc;": "\\^{O}",
	"&Otilde;": "\\~{O}",
	"&Ouml;": '\\"{O}',
	"&Oslash;": "\\O{}",
	"&OElig;": "\\OE{}",
	"&Scaron;": "\\v{S}",
	"&Ugrave;": "\\`{U}",
	"&Uacute;": "\\'{U}",
	"&Ucirc;": "\\^{U}",
	"&Uuml;": '\\"{U}',

	"&Yacute;": "\\'{Y}",
	"&Yuml;": '\\"{Y}',
	"&THORN;": "\\TH{}",
	"&agrave;": "\\`{a}",
	"&aacute;": "\\'{a}",
	"&acirc;": "\\^{a}",
	"&atilde;": "\\~{a}",
	"&auml;": '\\"{a}',
	"&aring;": "\\aa{}",
	"&aelig;": "\\ae{}",
	"&ccedil;": "\\c{c}",
	"&egrave;": "\\`{e}",
	"&eacute;": "\\'{e}",
	"&ecirc;": "\\^{e}",
	"&euml;": '\\"{e}',
	"&igrave;": "\\`{\i}",
	"&iacute;": "\\'{\i}",
	"&icirc;": "\\^{\i}",
	"&iuml;": '\\"{\i}',
	"&eth;": "\\dh{}",
	"&ntilde;": "\\~{n}",

	"&ograve;": "\\`{o}",
	"&oacute;": "\\'{o}",
	"&ocirc;": "\\^{o}",
	"&otilde;": "\\~{o}",
	"&ouml;": '\\"{o}',
	"&oslash;": "\\o{}",
	"&oelig;": "\\oe{}",
	"&scaron;": "\\v{s}",
	"&ugrave;": "\\`{u}",
	"&uacute;": "\\'{u}",
	"&ucirc;": "\\^{u}",
	"&uuml;": '\\"{u}',
	"&yacute;": "\\'{y}",
	"&thorn;": "\\th{}",
	"&yuml;": '\\"{y}',

	"&sigmaf;": "\\varsigma",

	"&alefsym;": "\\aleph",
	"&piv;": "\\varpi",
	"&real;": "\\Re",
	"&upsih;": "\\Upsilon",
	"&weierp;": "\\wp",
	"&image;": "\\Im",
	"&larr;": "\\leftarrow",
	"&uarr;": "\\uparrow",

	"&rarr;": "\\rightarrow",
	"&darr;": "\\downarrow",
	"&harr;": "\\leftrightarrow",
	"&crarr;": "\\hookleftarrow",
	"&lArr;": "\\Leftarrow",
	"&uArr;": "\\Uparrow",
	"&rArr;": "\\Rightarrow",
	"&dArr;": "\\Downarrow",
	"&hArr;": "\\Leftrightarrow",
	"&there4;": "\\therefore",
	"&sub;": "\\subset",
	"&sup;": "\\supset",
	"&nsub;": "\\not\\subset",
	"&sube;": "\\subseteq",
	"&supe;": "\\supseteq",
	"&oplus;": "\\oplus",
	"&otimes;": "\\otimes",
	"&perp;": "\\perp",
	"&sdot;": "\\cdot",
	"&lceil;": "\\lceil",
	"&rceil;": "\\rceil",
	"&lfloor;": "\\lfloor",
	"&rfloor;": "\\rfloor",
	"&lang;": "\\langle",
	"&rang;": "\\rangle",

	"&loz;": "\\lozenge",
	"&spades;": "\\spadesuit",
	"&clubs;": "\\clubsuit",
	"&hearts;": "\\heartsuit",
	"&diams;": "\\diamondsuit",

	# misc:
	"_": "\\_",
	"<p>|": "|",
	"|</p>": "|",
	"<br />": " \\hfill\\break ",
	"text-align: left; ": "",
	"padding-left: 60px; text-align: center;": "text-align: center;",
	'<span style="text-align: center; ': '<span style="'
}

GL = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
	"iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho",
	"sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"]
for l in GL:
	c = l.capitalize()
	swaps["&%s;"%(l,)] = "\\%s"%(l,)
	swaps["&%s;"%(c,)] = "\\%s"%(c,)

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
		"start": "<u>",
		"tex": "\\underline{%s}"
	},
	"img": {
		"start": '<img style="display: block; max-width: 100%;" src="../',
		"endstart": '" ',
		"end": ' />',
		"tex": "\\includegraphics[width=\\linewidth]{%s}",
		"sym": True,
		"startend": None
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
		"nostyle": True,
		"tex": " \\\\ %s "
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