from ..Element import Element

class SelfClosingElement(Element):

        @property
        def contentsAndCloser(self):
        	"""Self-closing has no contents"""
        	return ['/>'] 