from Module import Module
from html.Element import Element

class HtmlDocument(Module):

    def __init__(self):
        self.Head = Element('head')
        self.Body = Element('body')
        
    def Render(self):
        """Override this method to add stuff to the Container"""
        return self.Container.add(self.Head, self.Body)
    
    @property
    def Container(self):
        return Element('html')