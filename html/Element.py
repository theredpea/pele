#Node
from ..Node import Node
from ..Text import Text
from ..Fragment import Fragment
from ..IRenderable import IRenderable

#Builtin
import re
import itertools
import sys


          
class Element(IRenderable, Node):
        
    #HTML DOM distinctions
    _hasRef             = False
    _selfClosing        = False
    _blockElement       = False
    _hasBlockChildren   = False
    _onlyTextChildren   = True
    
    #Stylistic decisions
    _sortAttrs = True
    
    
    def __new__(cls, *args, **kwargs):
        tagName = (args and args[0]) or kwargs.get('tagName')
        try:
            import html.elements as elements
        except Exception as e:
            import elements
        
        subClass = getattr(elements, tagName and tagName.lower(), False)
        
        if cls is Element and subClass:
            #Route to the appropriate subclass for validation, etc
            #http://www.wellho.net/mouth/1146_-new-v-init-python-constructor-alternatives-.html
            #When would you use __new__?

            # 1. When you want you constructor to return an object 
            #of a different type to the class in which it is defined. 
            #For example, you have a class "animal" with subclasses "farmanimal" and "pet" 
            #and you want the animal cosntructor to be able to examine the data passed in to it 
            #and return an animal ... OR a farmanimal OR a pet depending on that data.
            return object.__new__(subClass, *args, **kwargs)         
        else:
            return object.__new__(cls, *args, **kwargs)
            
        
    def __init__(self, tagName='', *args, **kwargs):
        """Node("div", class="className", id="specialDiv")
        -> <div class="className" id ="specialDiv"></div>"""
        super(Element,self).__init__(*args, **kwargs)
        
        self._children = Fragment()
        self._attributes= {}
        self._classes = set()
        
        self.addAttribute(**kwargs)
        if tagName:
            self.parseTagName(tagName)
            
        self.add(*args)

    def Render(self):
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
        """Node.addAttribute('href', 'http://www.google.com')
        -> Node with 'href = 'http://www.google.com'

        Alternatate: Node.addAttribute(href='http://www.google.com')
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
                #from elementTypes import inline
                if not (isinstance(a,Text)):
                    self._onlyTextChildren = False
                if getattr(a, '_blockElement', False): 
                    #BlockElement._inlineElement = False
                    self._hasBlockChildren = True
            except Exception as e:
                pass
            return a
        
        #Make iterable for itertools.chain to work
        self._children.add(itertools.imap(_addParent,Fragment(argList, *args)))
        return self
    
    
    def addText(self, *args):
        return self.add(*args)
    
    _indentInline = False
    _pretty = True
    _indent = '  '
    
    def _joinableLevelIter(self):#, pretty=_pretty, indentInline = _indentInline, indent = _indent):
        """Produces iterable
        Node("div")._joinableLevelIter()
        -> ['<','div', ' ', '>', '</', 'div', '>']

        Used in stringing
        Based on idea that ''.join(iterOfStrings) is fastest way
        to construct big string; vs StringIO; alt StringBuilder
        """
        source = self._parent or self
        indentInline    = source._indentInline
        pretty          = source._pretty
        indent          = source._indent
            
        def _incrLevelAndIndex((index, child)):
            """Rather than relying on the Node @properties"""
            try:
                child._level = self._level+1
                child._index = index 
            except Exception as e:
                #A string?
                pass
            return child
        
            
        shouldIndent    =   (pretty                                #If pretty is False, dont worry about it
                                and not self._onlyTextChildren     #Dont indent if only text children
                                and (indentInline                  #False by default; may want to indent for clarity
                                    or self._hasBlockChildren))

        opener          =   itertools.chain(
                            ['<', self._tagName.lower()],
                            self._joinableAttrsIter())
        innerIndent     =   (['\n']+([indent]*(self._level+1))) if shouldIndent else []
        innerDedent     =   (['\n']+([indent]*(self._level))) if shouldIndent else []
        
        def _strWithIndent(child):
            result = (str(child),)
            try:
                if child._index!=0:
                    result = itertools.chain(innerIndent, result)
            except:
                pass
            return result
            
        closer          =   ['/>'] if self._selfClosing else itertools.chain(
                            ['>'],
                            innerIndent,
                            itertools.chain.from_iterable(
                                itertools.imap(_strWithIndent, 
                                    itertools.imap(_incrLevelAndIndex, enumerate(self._children))
                                )
                            ),
                            innerDedent,
                            ['</', self._tagName.lower(), '>'])
        
        
        return itertools.chain(opener, closer)
    
    def _joinableAttrsIter(self):
        """Produces iterable
        Node("div").addAttribute(href="http://www.github.com", class="open")
        ->['class', '="', 'open', '"', 'href="', 'http://www.github.com', '"']

        Used in stringing
        If self.sorted, puts them in sorted order
        Else whatever dictionary order
        """
        def _joinableAttrIter((k,v)):
            return [' ', str(k).strip(), '="', str(v).strip(), '"']
        
        if self._sortAttrs:
            attrs = sorted(self._attributes.items())
        else:
            attrs = self._attributes.items()

        return itertools.chain.from_iterable(itertools.imap(_joinableAttrIter, attrs))
                    
    def __str__(self):
        return ''.join(self._joinableLevelIter())
        
    def Render(self):
        return self
        
    #jQuery aliases
    attr = addAttribute
    append = add
    text = addText
