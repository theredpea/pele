                        #Used by Element __new__ to route to Element subclass
                            # - These become attrs of the elements module
                            # - No ambiguity in that context; elements is a module
                            # - <module 'pele.html.elements' from 'pele\html\elements\__init__.py'>
                        #Also can be used in import from html.elements import table
                            # - From pele.html.elements import span
                            # - print(span('hello world'))
from a import A         as a
from span import Span   as span
from area import Area   as area
from div import Div     as div
from table import Table as table
from p import P         as p
from ul import Ul       as ul
from li import Li       as li