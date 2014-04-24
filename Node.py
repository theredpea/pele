from Fragment import Fragment
    
class Node(object):
    """Has one parent;
    Unless root; not _parent
    Level represents _len() ******
    Index represents _parent._children.index(self)
    
    May have children
    
    Sufficient conditions to create a tree structure"""
    
    #Illustrate the purpose of this class
    #Shouldn't use for each Node in a tree; 
    #Repeats calculations
    @property
    def is_root(self):
        return not self._parent
        
    @property
    def index(self):
        """Which element in its sublings"""
        #http://stackoverflow.com/q/8197323/1175496
        #Be careful of exception; though it shouldn't happen
        if not self._parent:
            return 0
        else:
            #http://docs.python.org/2/glossary.html#term-hashable 
            #They equal themselves; it's taken care of
            return self._parent._children.index(self)
        
    @property
    def level(self):
        """How 'far away from the root';
        i.e. length of ancestor_chain"""
        if not self._parent:
            return 0
        else:
            return len(list(self.ancestor_chain))
            
    @property
    def ancestor_chain(self):
        """Recurse through each ancestor"""
        if not self._parent:
            return
        else:
            parent = self._parent
            while parent:
                yield parent
                try:
                    parent = parent._parent
                except Exception as e:
                    parent = None #Exit the loop
                    return
            
            
    def __init__(self, *args, **kwargs):

        self._parent = None
        self._level = 0
        self._index = 0
        self._children = []

