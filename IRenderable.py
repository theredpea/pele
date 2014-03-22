from Node import Node
from abc import ABCMeta, abstractmethod

class IRenderable:
    """Closest Python has to an interface? http://docs.python.org/2/library/abc.html"""
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def Render(self):
        """Python can't guarantee return type
        But, this is more than just interface;
        This method can provide implementation
        It's *not* a default implementation
        Subclasses must provide their own implementation
        However, their own implementation can super() this one"""
        return Node()
