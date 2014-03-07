import re
import itertools


class Node(object):
        
        
        def __init__(self, tagName, **kwargs):
                """Node("div", class="className", id="specialDiv")
                -> <div class="className" id ="specialDiv"></div>"""
                self._parent = None
                
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
                
                for prop,value in kwargs.items():
                        self.addAttribute(prop, value)
                return self

        def add(self, *args):

                def _addParent(a):
                        #Assign parents on an individual level
                        try:
                                a._parent = self
                        except:
                                pass
                        return a
                
                def _iter(a):
                        if not a:
                                #Filter out nulls, empty lists, etc
                                return []
                        try:
                                #Must be iterable for itertools.chain to work
                                iter(a)
                                return a
                        except:
                                return [a]
                
                #Consequence of making children a itertools.chain object;
                        #Once iterated, it is exhausted
                self._children = itertools.chain(self._children,
                                                        itertools.imap(_addParent, itertools.chain.from_iterable(
                                                                itertools.imap(_iter, args))))
                return self
        
        
        def addText(self, *args):
                return self.add(*args)
        
        #jQuery aliases
        attr = addAttribute
        append = add
        text = addText

        def __str__(self):
                selfClosing = False
                opener = ['<', self._tagName.lower(), ' ' ] + [''.join([prop.strip(), '="', val.strip(), '" ']) for prop, val in sorted(self._attributes.items())]
                closer = ['/>'] if selfClosing else (['>']+ [str(_) for _ in list(self.children)] + ['</', self._tagName, '>'])
                
                return ''.join(opener + closer)
        
        @property
        def children(self):
                #Since iterating the _children will empty it out
                self._children = list(self._children)
                return self._children
