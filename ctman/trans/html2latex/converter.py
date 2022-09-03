from .util import TABLE_FLAGS, flags, swaps, styles, cstyles, trans, Converter
from .header import Header

class H2L(Converter):
	def __init__(self, fragment, depth=0, swappers=swaps, flaggers=flags, styles=styles, cstyles=cstyles):
		Converter.__init__(self, fragment, depth, swappers, flaggers, styles, cstyles)
		self.header = Header()

	def translate(self):
		self.swapem()
		self.translation = trans(self.translation, "table", TABLE_FLAGS)
		self.bottomsup()
		self.translation = self.header(self.translation, self.depth)
		self.cleanup()
		return self.translation

	def cleanup(self):
		self.translation = self.translation.replace("{#}", "{\\#}")
		self.translation = self.translation.replace("NEWPAGE", # custom injection
			"\\newpage").replace("\\begin{flushleft}\\newpage\\end{flushleft}",
			"\\newpage")