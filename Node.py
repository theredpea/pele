from Fragment import Fragment
    
class Node(object):
    
    
    #Stylistic decisions
    _sortAttrs = True
    _prettyIndent = False
    _overrideParentPretty = False
    
    
    def __init__(self, *args, **kwargs):
        """Node("div", class="className", id="specialDiv")
        -> <div class="className" id ="specialDiv"></div>"""

        self._parent = None
        self._level = 0
        self._children = []

        

				
