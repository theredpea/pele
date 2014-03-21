from Element import Element

class BlockElement(Element):
        """Opposite of block element is inline element"""
        _blockElement = True

class SelfClosingElement(Element):
        _selfClosing = True

class HasRefElement(Element):
        _hasRef = True
        _refAttrs = ('action','cite','href','rel','rev','src')
