from .util import Converter

DXPB = """```{=openxml}
<w:p>
  <w:r>
    <w:br w:type="page"/>
  </w:r>
</w:p>
```"""

def dxtl(alignment):
	return '```{=openxml}\n<w:jc w:val="' + alignment + '">\n  %s\n</w:jc>\n```'

swaps = {
	"NEWPAGE": DXPB
}
flags = {
	"p": { "tex": "\n\n%s\n\n" }
}
styles = {
	"text-align": {
		"center": dxtl("center"),
		"right": dxtl("right"),
#		"left": dxtl("left")
	}
}

class H2X(Converter):
	def __init__(self, fragment, depth=0, swappers=swaps, flaggers=flags, styles=styles, cstyles={}, loud=True):
		Converter.__init__(self, fragment, depth, swappers, flaggers, styles, cstyles, loud)