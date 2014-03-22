import unittest
import timeit
from testElement import ElementTestCase
from ..html.elements import *


class ElementsConstructorTestCase(ElementTestCase):
        
    def test_str_output_matches_string(self):
        self.assertEqual(str(self.div), '<div class="className" id="idName"></div>')
        