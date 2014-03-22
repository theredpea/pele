from ..Element import Element
from pele.IRenderable import IRenderable

#TODO: Make an ABC for the Render method
class ViewModule(IRenderable):

    def Render(self):
        """Override this method to add stuff to the Container"""
        return self.Container
        
    @property
    def Container(self):
        """Override this property to return a different Container"""
        return Element('div')