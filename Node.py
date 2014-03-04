class Node(INode,IRenderable):
	def __init__(self, tagName):
		self._children = []
		self.parseTagName(tagName)
	def render(self):
		return self
	
	@property
	def children(self):
		if not self._children:
			self._children = Fragment()
		return self._children
	
	@children.setter
	def children(self, value):
		self._children = value

	@property
	def attributes(self):
		self.initAttributes();
		return self._attributes
