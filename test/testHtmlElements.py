import unittest
import timeit
from testElement import ElementTestCase
from html.elements import *


class ElementsValidationTestCase(ElementTestCase):
        
    def test_inline_validation(self):
        pass
        
class ElementsFluentConstructorTestCase(ElementTestCase):
        
    def setUp(self):
        _nav = {'Index':'/index','Contact': '/contact'}
        def _nav_link((text,link)):
            return li(a(text, href=link))
        self._ul_string ='<ul>'\
        '<li><a href="/index">Index</a></li>'\
        '<li><a href="/contact">Contact</a></li>'\
        '</ul>'

        self._ul_with_generation = ul((li(a(text, href=link)) for text,link in _nav.items()))
        self._ul_with_map = ul(map(_nav_link, _nav.items()))

        #self._ul_with_generation._pretty = True
        #self._ul_with_map._pretty = True
        #self._ul_with_generation._indentInline = True
        #self._ul_with_map._indentInline = True

    def test_fluency(self):
        d = div(
                span('hello', 
                    a('world', 
                        href='http://en.wikipedia.org/wiki/Hello_world_program')
                    )
                )
        #print(d)
        self.assertTrue(d)
    
    def test_generator(self):
        self.assertEqual(str(self._ul_with_generation), self._ul_string)

    def test_map(self):
        self.assertEqual(str(self._ul_with_map), self._ul_string)
        
        