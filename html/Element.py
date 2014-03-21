from Node import Node
from Text import Text
import re
import itertools

def node(*args, **kwargs):
        return Element(*args, **kwargs)

class Element(Node):
                
        #HTML DOM distinctions
        _hasRef = False
        _selfClosing = False
        _blockElement = False
        
        def __init__(self, tagName='', *args, **kwargs):
                
                super(Element,self).__init__(*args, **kwargs)
                
                #TODO: Some inheritance:
                #http://www.w3.org/TR/DOM-Level-2-HTML/html.html#ID-22445964"""
                self._attributes= {}
                
                self._classes = set()
                
                self.addAttribute(**kwargs)
                
                if tagName:
                        self.parseTagName(tagName)

                

        def render(self):
                return self

        def parseTagName(self, tagExpression):
                """Node.parseTagName("div.className#idName")
                -> Node with class of "className" and id attribute of "idName"
                Equivalent to Node("div").addClass("className").addAttribute("id", "idName")
                
                Accepts string in CSS3 syntax for ID and classes
                Creates a Node that would match the selector

                CSS3 Attribute syntax [property=value] is *not supported*"""
                
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

                Alternatate: Node.addClass("newClassName", "anotherNewClass")

                Uses a set to store classes internally (same for other? http://www.crummy.com/software/BeautifulSoup/bs4/doc/#multi-valued-attributes)
                Splits on spaces
                Ignores falsey classes
                Otherwise accepts user input (case-sensitive)"""
                if not newClass and not args:
                        return self

                self._classes.update(itertools.chain.from_iterable([c.split(' ') for c in ([newClass] + list(args)) if c]))
                self._attributes['class'] = ' '.join(self._classes)
                return self

        @property
        def id(self):
                return self._attributes.get('id', None)
        
        @property
        def classAttr(self):
                return ' '.join(self._classes)
        @property
        def name(self):
                return self._tagName
        
        def addAttribute(self, prop=None, value=None, **kwargs):
                """Node.addAttribute("href", "http://www.google.com")
                -> Node with "href = 'http://www.google.com'

                Alternatate: Node.addAttribute(href="http://www.google.com")
                Order doesn't matter
                Calls self.addClass for any attribute named class"""
                if not prop and not kwargs:
                        return self
                elif prop and value:
                        kwargs[prop] = value

                if 'class' in kwargs:
                        #Set Logic
                        self.addClass(kwargs['class'])
                        del kwargs['class']
        
                self._attributes.update(kwargs)
                
                
                return self

        def add(self, argList=[], *args):
                """div.add(Node("p").add("Paragraph content"))
                -> Node where _children includes p;
                Will render <div><p>Paragraph content</p></div>

                """
                def _addParent(a):
                        #Assign parents on an individual level
                        try:
                                a._parent = self
                                a._level = self._level+1
                        except:
                                pass
                        return a
                
                def _iter(a):
                        if isinstance(a, str):
                                return [Text(a)]
                        try:
                                #Must be iterable for itertools.chain to work
                                iter(a)
                                return a
                        except:
                                return [a]
                
                self._children = itertools.chain(self._children,
                                                        itertools.imap(_addParent,
                                                                itertools.ifilter(None,      #Filter out empty
                                                                        itertools.chain(_iter(argList), itertools.chain.from_iterable(  #Support two syntaxes
                                                                                itertools.imap(_iter,args)))))) #Make iterable for itertools.chain to work
                return self
        
        
        def addText(self, *args):
                return self.add(*args)
        
        def _joinableLevelIter(self, level=0, _prettyIndent = False):
                """Produces iterable
                Node("div")._joinableLevelIter()
                -> ['<','div', ' ', '>', '</', 'div', '>']

                Used in stringing
                Based on idea that ''.join(iterOfStrings) is fastest way
                to construct big string; vs StringIO; alt StringBuilder
                """
                if self._parent and not self._overrideParentPretty:
                        self._prettyIndent = self._parent._prettyIndent
                        
                def _joinable(a):
                        try:
                                return a._joinableLevelIter(level+1, self._prettyIndent)
                        except:
                                return [str(a)]
                        
                
                opener = itertools.chain(
                                ['<', self._tagName.lower(), ' ' ],
                                itertools.chain.from_iterable(self._joinableAttrIter()))
                
                closer = ['/>'] if self._selfClosing else itertools.chain(
                                ['>'],
                                itertools.chain.from_iterable(itertools.imap(_joinable, self.children)),
                                ['</', self._tagName, '>'])


                
                startIndent = (['\n']+['\t']*self._level) if (self._parent and self._prettyIndent) else []
                endIndent = (['\n']+['\t']*(self._level-1)) if (self._parent and self._prettyIndent) else []
                
                return itertools.chain(startIndent, opener, closer, endIndent)
        
        def _joinableAttrIter(self):
                """Produces iterable
                Node("div").addAttribute(href="http://www.github.com", class="open")
                ->['class', '="', 'open', '"', 'href="', 'http://www.github.com', '"']

                Used in stringing
                If self.sorted, puts them in sorted order
                Else whatever dictionary order
                """
                def _attr((k,v)):
                        return [str(k).strip(), '="', str(v).strip(), '" ']
                
                if self._sortAttrs:
                        attrs = sorted(self._attributes.items())
                else:
                        attrs = self._attributes.items()

                return itertools.imap(_attr, attrs)
                                      
        def __str__(self):
                return ''.join(self._joinableLevelIter())
        
        @property
        def children(self):
                #Since iterating the _children will empty it out
                self._children = list(self._children)
                return self._children

        #jQuery aliases
        attr = addAttribute
        append = add
        text = addText
