from ..Node import Node
from Element import Element

#Element Types
from elementTypes import BlockElement, SelfClosingElement, HasRefElement

#Elements
import elements


def node(*args, **kwargs):
		"""Convenience method like the Node method inside Modules
		Not to be confused with the Node class
		Convenient because it is short; four letters; and lowercase
		Consider another short method name. """
		return Element(*args, **kwargs)