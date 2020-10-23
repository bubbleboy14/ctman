from cantools import config
from .util import TABLE_FLAGS, trans, swaps, nextlast
from .header import Header
from .fragment import Fragment

class H2L(object):
	def __init__(self, fragment, depth):
		self.fragment = fragment
		self.depth = depth
		self.header = Header()

	def translate(self):
		self.swaps()
		self.translation = trans(self.translation, "table", TABLE_FLAGS)
		self.bottomsup()
		self.translation = self.header(self.translation, self.depth)
		self.cleanup()
		return self.translation

	def swaps(self):
		h = self.fragment
		for swap in swaps:
			h = h.replace(swap, swaps[swap])
		self.translation = h

	def bottomsup(self):
		h = self.translation
		flag = nextlast(h, flags)
		while flag:
			h = trans(h, flag)
			flag = nextlast(h, flags)
		self.translation = h

	def cleanup(self):
		self.translation = self.translation.replace("{#}", "{\\#}")