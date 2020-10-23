from cantools import config
from .header import Header
from .fragment import Fragment

class H2L(object):
	def __init__(self, fragment, depth):
		self.fragment = fragment
		self.depth = depth
		self.header = Header()

	def translate(self):
		self.swaps()
		self.trans("table", TABLE_FLAGS)
		self.bottomsup()
		self.translation = self.header(self.translation, self.depth)
		self.cleanup()
		return self.translation

	def bottomsup(self):
		h = self.translation
		flag = nextlast(h, flags)
		while flag:
			h = trans(h, flag)
			flag = nextlast(h, flags)
		flag = nextlast(h, liners)
		while flag:
			h = trans(h, flag, liners[flag])
			flag = nextlast(h, liners)
		self.translation = h

	def cleanup(self):
		self.translation = self.translation.replace("{#}", "{\\#}")