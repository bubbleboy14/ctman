from cantools import config
from .util import swaps
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
		flag = nextlast(h, liners)
		while flag:
			h = trans(h, flag, liners[flag])
			flag = nextlast(h, liners)
		self.translation = h

	def cleanup(self):
		self.translation = self.translation.replace("{#}", "{\\#}")