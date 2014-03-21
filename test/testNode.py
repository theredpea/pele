import unittest
import timeit
from html import Element

class ElementTestCase(unittest.TestCase):
    def setUp(self):
        self.div = Element("div#idName.className")
        

class ElementStringTestCase(ElementTestCase):
        
    def test_str_output_matches_string(self):
        self.assertEqual(str(self.div), '<div class="className" id="idName" ></div>')
        
    def test_str_output_matches_new_Element_string(self):
        #Really testing that CSS3 constructor is same as addAttributes;
        self.assertEqual(str(self.div), str(Element('div').addAttribute('id', 'idName').addAttribute('class','className')))
        
    def test_str_output_pretty_indent_matches_string(self):
        _divWithPara = Element("div").add(Element("p"))
        _divWithPara._prettyIndent = True
        self.assertEqual(str(_divWithPara), '\n<div >\n\t<p ></p>\n</div>\n')
        
    def test_str_output_pretty_indent_matches_new_Element_string(self):
        self.assertEqual(str(self.div), str(Element('div').addAttribute('id', 'idName').addAttribute('class','className')))
        
class ElementParseTagTestCase(ElementTestCase):
    def setUp(self):
        self.abcDiv = Element("div.a.b.c")
        
    def test_has_classes(self):
        self.assertIn('class', self.abcDiv._attributes)
        self.assertEqual(self.abcDiv._classes, set('abc'))
        
    def test_has_id(self):
        self.assertIn('class', self.abcDiv._attributes)
        self.assertEqual(self.abcDiv._classes, set('abc'))

class ElementAddTestCase(ElementTestCase):
        
    def test_number_children_equal_number_add(self):
        _num=3
        
        self.div.add([Element("p")]*_num)
        self.assertEqual(len(self.div.children), _num)

        
    def test_none_ignored(self):
        _children = ['text', None, 'text']
        _truthyChildren = filter(None, _children)
        
        div = Element("div")
        div.add(*_children)
        
        self.assertEqual(len(div.children), len(_truthyChildren))

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
        self.a.addAttribute("href", "http://www.google.com")
        self.assertIn("href", self.a._attributes)
        self.assertEqual(self.a._attributes["href"], "http://www.google.com")

    def test_attributes_override(self):
        _1 = 'firstIdName'
        _2 = 'secondIdName'
        _3 = 'thirdIdName'
        
        self.div = Element('div#{0}#{1}'.format(_1, _2))
        self.assertIsNotNone(self.div._attributes.get('id'))
        
        #That secondIdName overrode firstIdName in constructor
        self.assertNotEqual(self.div._attributes['id'],_1)
        self.assertEqual(self.div._attributes['id'], _2)
        
        #That thirdIdName overrode secondIdName in addAttribute
        self.div.addAttribute('id', _3)
        self.assertNotEqual(self.div._attributes['id'], _2)
        self.assertEqual(self.div._attributes['id'], _3)
        
    def test_id_property(self):
        _i = 'idValue'
        div = Element('div#{}'.format(_i))
        self.assertEqual(div.id, _i)
        self.assertIsNotNone(div._attributes.get('id'))
        self.assertEqual(div.id, div._attributes.get('id'))
        
class ElementSpeedTestCase(ElementTestCase):
    
    class C(object):
            def __init__(self, **kwargs):
                    self.__dict__.update(kwargs)
                    
    def rowMaker(self, o):
        return Element("tr").append((Element("td").append(v) for k,v in sorted(o.__dict__.items())))
    
    def headerMaker(self, o):
        return Element("tr").append((Element("th").append(k) for k in sorted(o.__dict__.keys())))

    def test_timing_large_table(self):
        pass
