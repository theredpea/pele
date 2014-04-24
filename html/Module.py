from IRenderable import IRenderable
from html.Element import Element
import inspect

class Module(IRenderable):

    def __init__(self):
        """http://stackoverflow.com/a/1401900/1175496"""
        self._Container = Element("div").AddClass(*[t.__name__ for t in inspect.getmro(self)])

    @property
    def Container(self):
        """The Element that represents markup for the module.
        No need for a 'CreateContainer' method; just put any such logic in the getter"""
        return self._Container

    @Container.setter
    def Container(self, value):
        self._Container = value

    
    def Render(self):
        return self.Container
