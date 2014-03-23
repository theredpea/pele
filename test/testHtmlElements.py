import unittest
import timeit
from testElement import ElementTestCase
from ..html.elements import *


class ElementsValidationTestCase(ElementTestCase):
        
    def test_inline_validation(self):
        pass
        
class ElementsFluentConstructorTestCase(ElementTestCase):
        
    def test_fluency(self):
        d = div(
                span('hello', 
                    a('world', 
                        href='http://en.wikipedia.org/wiki/Hello_world_program')
                    )
                )
        print(d)
        self.assertTrue(d)
        