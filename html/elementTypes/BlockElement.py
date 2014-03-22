from ..Element import Element

class BlockElement(Element):
    """Block can contain Inline
    Inline cannot contain Block
    Opposite of see elementTypes.InlineElement"""
    _blockElement = True
    _inlineElement = False