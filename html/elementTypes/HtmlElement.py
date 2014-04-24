from ..Element import Element
import itertools

class HtmlElement(Element):

    def __new__(cls, *args, **kwargs):
        """Overriding the Element 'router' __new__ method
        Which creates an instance of HtmlElement if
        it can find a type whose __name__ matches tagName"""
        return object.__new__(cls, *args, **kwargs)
        
    def __init__(self, *args, **kwargs):
        """Taking tagName from __class__.__name__
        and Removing the tagName from list of args so Element.__init__ doesn't add it"""
        tagName= self.__class__.__name__.lower()
        
        removeTags = lambda x: not isinstance(x, str) or x.lower()!=tagName.lower()
        args = itertools.ifilter(removeTags, args)
        super(HtmlElement, self).__init__(tagName, *args, **kwargs)