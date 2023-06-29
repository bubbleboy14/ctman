from ctman.util import getstart
from .rules import *
from ..util import nextlast, trans, Converter

#
# tables
#

TSEP = '</tr>'
TBL = "\\tabby{%s}{%s}"

def clean(data):
	data = data.replace("\n", " ")
	for c in "#$%^":
		data = data.replace(c, "\\%s"%(c,))
	if "<" in data:
		for flag in tflags:
			data = trans(data, flag, tflags[flag])
#		data = "\\Centerstack{%s}"%(data,)
	return data

def row(chunk):
	return [clean(part.split(">", 1)[1].split("</td>")[0]) for part in chunk.split('<td')[1:]]

def table(seg):
	rowz = list(map(row, seg.split(TSEP)))
	numcols = len(rowz[0])
	if "img" in seg:
		iorig = flags["img"]
		seg = trans(seg, "img", {
			"sym": iorig["sym"],
			"start": iorig["start"],
			"endstart": iorig["endstart"],
			"startend": iorig["startend"],
			"end": iorig["end"],
			"tex": "\\includegraphics[width=" + str(1.0 / numcols)[:3] + "\\linewidth]{%s}"
		}, loud=True)
	rowz = list(map(row, seg.split(TSEP)))
#	return TBL%(numcols * "C", "\\\\\n\n".join([" & ".join(r) for r in rowz]))
	return TBL%("| %s |"%(" | ".join(numcols * "C"),),
		"\n\\hline\n%s\n\\\\ \\hline"%("\\\\\n\\hline\n".join([" & ".join(r) for r in rowz]),))
#	else:
#		return "\n".join(map(bartable, rowsets(rowz)))

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