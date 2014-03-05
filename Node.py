import re

def alias(*args):
        aliases = args
        def decorator(f):
                print(f)
                print(type(f))
                def replacement(*args, **kwargs):
                        f(*args, **kwargs)
                return replacement
        return decorator

class Node(object):
        
        floating = None
        
        def __init__(self, tagName, **kwargs):
                """Node("div", class="className", id="specialDiv")
                -> <div class="className" id ="specialDiv"></div>"""
                self._children = []
                self._attributes = kwargs
                self.parseTagName(tagName)

        def render(self):
                return self

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
                -> Node with class="newClassName anotherNewClass

                Alternatate: Node.addClass("newClassName", "anotherNewClass")"""
                if not newClass and not args:
                        return self
                
                newClassList = [c for c in (newClass.split(' ') + list(args)) if c and c not in self._attributes.setdefault('class', '')]
                self._attributes['class']+= ' ' + ' '.join(newClassList)
                self._attributes['class'] = self._attributes['class'].strip() #Avoid starting space: class=' a b c'
                return self
        
        @alias('attr')        
        def addAttribute(self, prop=None, value=None, **kwargs):
                """Node.addAttribute("href", "http://www.google.com")
                -> Node with "href = 'http://www.google.com'

                Alternatate: Node.addAttribute(href="http://www.google.com")"""
                if not prop:
                        if not value and not kwargs:
                                return self
                else:
                        if value:
                                self._attributes[prop]=str(value).strip()
                        #elif prop in self._attributes:
                        #        del self._attributes[prop]
                
                for prop,value in kwargs.items():
                        self.addAttribute(prop, value)
                return self
        
                                

        def __str__(self):
                selfClosing = False
                opener = ['<', self._tagName, ' ' ] + [''.join([prop.strip(), '="', val.strip(), '" ']) for prop, val in sorted(self._attributes.items())]
                closer = ['/>'] if selfClosing else (['>']+[str(c) for c in self._children] + ['</', self._tagName, '>'])
                
                return ''.join(opener + closer)
