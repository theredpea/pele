from ElementTypes import SelfClosingElement, HasRefElement

class Input(SelfClosingElement, HasRefElement):
        _tagName="input"
        _validTypes = ('text', 'email')
        
        def __init__(self, *args, **kwargs):
                super(SelfClosingElement, self).__init__(*args, **kwargs)

        def addAttribute(self, *args, **kwargs):
                _defaults = dict(type='text')
                _defaults.update(kwargs)
                
                super(SelfClosingElement, self).addAttribute(*args, **_defaults)
                
                self._type = self._attributes.get('type')
                return self
        
        def _validate(self):
                assert self._type, 'Input needs a type'
                assert self._type in Input._validTypes, 'Input needs a valid type, {0} not in {1}'.format(self._type, Input._validTypes)

                return True
        
class Area(SelfClosingElement, HasRefElement):
        _tagName="area"

class Img(SelfClosingElement, HasRefElement):
        _tagName="img"

class Link(SelfClosingElement, HasRefElement):
        _tagName="link"

