try:
        #Python 3+
        import html as escaper
except:
        #Python 2
        from xml.sax import saxutils as escaper

class Text(object):
        def __init__(self, text='', leaveRaw = False):
                self._isEncoded = not leaveRaw
                self._value = text
                #TODO: Node
                self._parent = None

        @property
        def _joinableIter(self):
                return [str(self)]
        
        def __str__(self):
                if self._isEncoded:
                        try:
                                return escaper.escape(self._value) #quote_value=True; only works for html
                        except:
                                pass
                return self._value
