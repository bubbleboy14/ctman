from .util import Converter

DXPB = """```{=openxml}
<w:p>
  <w:r>
    <w:br w:type="page"/>
  </w:r>
</w:p>
```"""
DXPA = """```{=openxml}
<w:p>
  <w:pPr>
    <w:jc w:val="ALIGNMENT"/>
  </w:pPr>
  <w:r><w:t>%s</w:t></w:r>
</w:p>
```"""

def dxta(alignment):
	return DXPA.replace("ALIGNMENT", alignment)

swaps = {
	"NEWPAGE": DXPB
}
flags = {
	"p": {
		"strip": ["b", "br"],
		"tex": "\n\n%s\n\n",
		"sanswap": {
			"<b>": '<w:b w:val="true"/>',
			"</b>": '<w:b w:val="false"/>',
			"<br>": '</w:t><w:br/><w:t>'
		}
	}
}
styles = {
	"text-align": {
		"center": dxta("center"),
		"right": dxta("right"),
#		"left": dxta("left")
	}
}

class H2X(Converter):
	def __init__(self, fragment, depth=0, swappers=swaps, flaggers=flags, styles=styles, cstyles={}, loud=True):
		Converter.__init__(self, fragment, depth, swappers, flaggers, styles, cstyles, loud)