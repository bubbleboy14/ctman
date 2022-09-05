from .util import TABLE_FLAGS, flags, swaps, styles, cstyles, trans, Converter
from .header import Header

linestrips = ["NEWPAGE"]
ifswaps = {
	"\\begin{center}": {
		" \\hfill\\break ": " \\\\ "
	}
}

class H2L(Converter):
	def __init__(self, fragment, depth=0, swappers=swaps, flaggers=flags, styles=styles, cstyles=cstyles, linestrips=linestrips, loud=False):
		Converter.__init__(self, fragment, depth, swappers, flaggers, styles, cstyles, linestrips, loud)
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
		self.translation = self.translation.replace("NEWPAGE", "\\newpage")
		self.ifswaps()

	def ifswaps(self):
		lines = []
		for line in self.translation.split("\n"):
			for swap in ifswaps:
				if swap in line:
					for k, v in ifswaps[swap].items():
						line = line.replace(k, v)
			lines.append(line)
		self.translation = "\n".join(lines)