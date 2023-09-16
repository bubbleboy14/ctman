from ctman.util import getstart
from .rules import *
from ..util import nextlast, trans, Converter

#
# tables
#

TSEP = '</tr>'
TBL = "\\begin{tabular}{%s}%s\\end{tabular}"

def clean(data):
	data = data.replace("\n", " ")
	for c in "#$%^":
		data = data.replace(c, "\\%s"%(c,))
	if "<" in data:
		for flag in tflags:
			data = trans(data, flag, tflags[flag])
	if "\\\\" in data:
		data = "\\Centerstack{%s}"%(data,)
	return data

def row(chunk):
	return [clean(part.split(">", 1)[1].split("</td>")[0]) for part in chunk.split('<td')[1:]]

def table(seg):
	print()
	print("table processing:", seg)
	print()
	preamble = ""
	if not seg.startswith("<tr"):
		preamble, seg = seg.split("<tr", 1)
		seg = "<tr%s"%(seg,)
		print("extracted preamble:", preamble)
	rowz = list(map(row, seg.split(TSEP)))
	numcols = len(rowz[0])
	colstr = "%s\\linewidth"%(str(1.0 / numcols)[:4],)
	colper = "p{%s}"%(colstr,)
	if "img" in seg:
		iorig = flags["img"]
		seg = trans(seg, "img", {
			"sym": iorig["sym"],
			"start": iorig["start"],
			"endstart": iorig["endstart"],
			"startend": iorig["startend"],
			"altstartend": iorig["altstartend"],
			"end": iorig["end"],
			"tex": "\\includegraphics[width=" + colstr + "]{%s}"
		}, loud=True)
		rowz = list(map(row, seg.split(TSEP)))
	return preamble + TBL%("| %s |"%(" | ".join(numcols * [colper])),
		"\n\\hline\n%s\\\\\n\\hline\n"%("\\\\\n\\hline\n".join([" & ".join(r) for r in rowz]),))

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