from ..Element import Element

class InlineElement(Element):
    """Opposite of elementTypes.BlockElement"""
    _blockElement = False
    _inlineElement = True