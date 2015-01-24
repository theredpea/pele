import inspect

from ...IRenderable import IRenderable
from ...html.Element import Element


class Module(IRenderable):

    def __init__(self):
        """http://stackoverflow.com/a/1401900/1175496
        https://docs.python.org/2/library/inspect.html#inspect.getmro
        Creates the default _Container
        Doesn't add class name to data-module-name;
        Instead, puts it in Class, to support "object-oriented CSS"""
        mro_list = [t.__name__ for t in inspect.getmro(type(self))]
        for irrelevant in ('object', 'IRenderable'):
            try:
                mro_list.remove(irrelevant)
            except:
                pass

        self._Container = Element("div").AddClass(*mro_list)

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
