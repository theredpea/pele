from ..Element import Element

class HasRefElement(Element):
        """Can validate its ref;
        And potentially perform additional path processing; i.e. replace "~" with some domain"""
        _refAttrs = ('action','cite','href','rel','rev','src')
        #_hasRef = True
