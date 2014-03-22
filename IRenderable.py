from Node import Node
from abc import ABCMeta, abstractmethod

class IRenderable:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def Render(self):
        return Node()
