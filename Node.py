import re

class Node(object):
        
        floating = None
        
        def __init__(self, tagName, **kwargs):
                self._children = []
                self._attributes = kwargs
                self.parseTagName(tagName)

        def render(self):
                return self

        @property
        def children(self):
                if not self._children:
                        self._children = Fragment()
                return self._children

        @children.setter
        def children(self, value):
                self._children = value

        @property
        def attributes(self):
                self.initAttributes();
                return self._attributes

        def parseTagName(self, tagExpression):
                """Node.parseTagName("div.className#idName")
                -> Node with class of "className" and id attribute of "idName"
                Equivalent to Node("div").addClass("className").addAttribute("id", "idName")
                
                Accepts string in CSS3 syntax for ID and classes
                Creates a Node that would match the selector"""
                
                firstDelim = None
                for match in re.finditer('\.(?P<class>\w*)|#(?P<id>\w*)', tagExpression):
                        firstDelim = firstDelim or match.start()
                        self.addClass(match.group('class'))
                        self.addAttribute('id', match.group('id'))

                self._tagName = tagExpression[:firstDelim]
                
                assert self._tagName, "Need a tagName, could not find in {0}".format(tagExpression)
                                      
        def addClass(self, newClass=None, *args):
                """Node.addClass("newClassName anotherNewClass")
                -> Node with class="newClassName anotherNewClass"""
                if not newClass and not args:
                        return self
                
                newClassList = [c for c in (newClass.split(' ') + list(args)) if c and c not in self._attributes.setdefault('class', '')]
                self._attributes['class']+= ' ' + ' '.join(newClassList)
                return self
                
        def addAttribute(self, prop=None, value=None, **kwargs):
                """Node.addClass("newClassName anotherNewClass")
                -> Node with class="newClassName anotherNewClass"""
                if not prop:
                        if not value and not kwargs:
                                return self
                else:
                        if value:
                                self._attributes[prop]=value
                        #elif prop in self._attributes:
                        #        del self._attributes[prop]
                
                for prop,value in kwargs.items():
                        self.addAttribute(prop, value)
                return self
        
                                

