from Text import Text

import itertools

def _iter(a):
        if isinstance(a, str):
                return [Text(a)]
        try:
                #Must be iterable for itertools.chain to work
                iter(a)
                return a
        except:
                return [a]
                
class Fragment(list):
    """Fragment: a collection on nodes. 
    Use this when you don't have a parent element"""

    def __init__(self, argList = [], *args, **kwargs):
        #TypeError: list() takes at most 1 argument (2 given)
        fragItems = itertools.ifilter(None, #Filter out empty
                                        itertools.chain(_iter(argList), itertools.chain.from_iterable(  #Support two syntaxes
                                            itertools.imap(_iter,args))))
                                                                                
        super(Fragment, self).__init__(fragItems)

    def __iterFragItems__(self):
        """Replaces the itertools.chain.from_iterable(itertools.imap(_joinable, self))"""
        for fragItem in super(Fragment,self).__iter__():
            
            try:
                fragIter = fragItem._joinableLevelIter(self._prettyIndent)
            except:
                fragIter = [str(fragItem)]
                    
            for fragIterItem in fragIter:
                yield fragIterItem
                
    def __str__(self):
        return ''.join(map(str,self.__iterFragItems__()))