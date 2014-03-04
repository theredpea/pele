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

        tagDelims = ('.', '#')
        def parseTagName(self, tagName):
                """Node.parseTagName("div.className#id") -> Node
                Accepts string in CSS3 syntax for ID and classes
                Creates a Node that would match the selector"""                #http://stackoverflow.com/a/4664889/1175496
                [(m.start(), m.end()) for m in re.finditer('[#\.][^#\.]*', e)]
                #[(3, 6), (6, 12)]
                while found:
                        
                return self._attributes
