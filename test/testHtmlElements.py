import unittest
import timeit
from testElement import ElementTestCase
from ..html.elements import *


class ElementsConstructorTestCase(ElementTestCase):
        
    def test_str_output_matches_string(self):
        self.assertEqual(str(self.div), '<div class="className" id="idName"></div>')
        
class ElementAddTestCase(ElementTestCase):
        
    def test_number_children_equal_number_add(self):
        _num=3
        
        self.div.add([Element("p")]*_num)
        self.assertEqual(len(self.div._children), _num)

        
    def test_none_ignored(self):
        _children = ['text', None, 'text']
        _truthyChildren = filter(None, _children)
        
        div = Element("div")
        div.add(*_children)
        
        self.assertEqual(len(div._children), len(_truthyChildren))

    def test_arg_expansion_equals_single_iter_arg(self):
        _gen = (Element("p").add(a) for a in 'NATE')
        _list = list(_gen)
        _tag = "div"

        div_expansion =     Element(_tag).add(*_list)
        div_single_arg =    Element(_tag).add(_list)
            
        self.assertEqual(str(div_expansion), str(div_single_arg))

        
class ElementAddAttributeTestCase(ElementTestCase):
    def setUp(self):
        self.a = Element("a")

    def test_add_inserts(self):
        _val =  'http://www.google.com'
        _attr= 'href'
        self.a.addAttribute(_attr,_val)
        self.assertIn(_attr, self.a._attributes)
        self.assertEqual(self.a._attributes[_attr], _val)

    def test_attributes_override(self):
        _1 = 'firstIdName'
        _2 = 'secondIdName'
        _3 = 'thirdIdName'
        
        self.div = Element('div#{0}#{1}'.format(_1, _2))
        self.assertIsNotNone(self.div._attributes.get('id'))
        
        msg='secondIdName overrode firstIdName in constructor'
        self.assertNotEqual(self.div._attributes['id'],_1)
        self.assertEqual(self.div._attributes['id'], _2)
        
        msg='thirdIdName overrode secondIdName in addAttribute'
        self.div.addAttribute('id', _3)
        self.assertNotEqual(self.div._attributes['id'], _2)
        self.assertEqual(self.div._attributes['id'], _3)
        
    def test_id_property(self):
        _i = 'idValue'
        div = Element('div#{0}'.format(_i))
        self.assertEqual(div.id, _i)
        self.assertIsNotNone(div._attributes.get('id'))
        self.assertEqual(div.id, div._attributes.get('id'))
        
class ElementSpeedTestCase(ElementTestCase):
    
    class C(object):
        """A utility class so kwargs can be closer to a JSON object
        Imparts all its properties to this __dict__"""
        def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
                    
    def rowMaker(self, o):
        return Element("tr").append((Element("td").append(v) for k,v in sorted(o.__dict__.items())))
    
    def headerMaker(self, o):
        return Element("tr").append((Element("th").append(k) for k in sorted(o.__dict__.keys())))

    def test_timing_large_table(self):
        pass
