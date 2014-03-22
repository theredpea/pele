from Element import Element

class HtmlElement(Element):

    def __new__(cls, *args, **kwargs):
        #print('HtmlElement.new {0} {1}'.format(args, kwargs))
        """Overriding the Element 'router' __new__ method
        Which creates an instance of HtmlElement if
        it can find a type whose __name__ matches tagName"""
        return object.__new__(cls, *args, **kwargs)
        
    def __init__(self, *args, **kwargs):
        #print('HtmlElement.init {0} {1}'.format(args, kwargs))
        tagName= self.__class__.__name__.lower()
        super(HtmlElement, self).__init__(tagName, *args, **kwargs)