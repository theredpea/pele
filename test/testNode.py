import unittest
import timeit
import operator
import itertools

from testElement import ElementTestCase
from pele.html.Element import Element
from pele.Fragment import Fragment

class NodeFundamentelsTestCase(ElementTestCase):
    def setUp(self):
        #Tree test
        self._first_a = Element('a')
        self._second_a = Element('a')
        self._both_a = Fragment(self._first_a, self._second_a)
        self._span = Element('span', self._both_a)
        self._div = Element('div', self._span)
        
        #Inline test
        self._open = Text('open ')
        self._link = Element('a', 'and', href='http://www.wikipedia.org')
        self._close = Text(' close')
        self._text = Fragment(self._open, self._link, self._close)
        self._text_span = Element(span, self._text)
        
        
    def test_level(self):
        self.assertEqual(self._first_a.level, 2)
        
    def test_index(self):
        self.assertEqual(self._second_a.index, 1)
        
    def test_root(self):
        self.assertTrue(self._div.is_root)
        
    def test_ancestor_chain(self):
        _get_tag_name = operator.attrgetter('_tagName')
        _first_ancestors_tags = tuple(itertools.imap(_get_tag_name, self._first_a.ancestor_chain))
        _second_ancestors_tags = tuple(itertools.imap(_get_tag_name, self._second_a.ancestor_chain))
        
        self.assertEqual(self._first_a.level, len(_first_ancestors_tags))
        self.assertEqual(_first_ancestors_tags, ('span', 'div'))
        self.assertEqual(_first_ancestors_tags, _second_ancestors_tags)
    