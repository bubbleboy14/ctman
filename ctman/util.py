#<p><span style="color: #ff0000;">this is it!</span></p>

sflag = '<span style="color: #'
slen = len(sflag)
eflag = "</span>"
elen = len(eflag)
mflag = ';">'
ltmp = "\\textcolor[HTML]{%s}{%s}"

def colfix(h):
	while sflag in h:
		start = h.index(sflag)
		end = h.index(eflag)
		[c, t] = h[start + slen:end].split(mflag)
		h = h[:start] + ltmp%(c, t) + h[end + elen:]
	return h