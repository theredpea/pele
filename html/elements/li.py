from ..elementTypes import htmEl, block

class Li(htmEl, block):
    pass
    
    def validate(self):
        assert self._parent and self._parent._tagName.lower() == 'ul'