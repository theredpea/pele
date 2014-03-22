import unittest
import timeit
from ..html.Element import Element

class ElementTestCase(unittest.TestCase):
    def setUp(self):
        self.div = Element("div#idName.className")
        

class ElementStringTestCase(ElementTestCase):
        
    def test_str_output_matches_string(self):
        self.assertEqual(str(self.div), '<div class="className" id="idName"></div>')
        
    def test_str_output_matches_new_Element_string(self):
        #Really testing that CSS3 constructor is same as addAttributes;
        self.assertEqual(str(self.div), str(Element('div').addAttribute('id', 'idName').addAttribute('class','className')))
        
    def test_str_output_pretty_indent_matches_string(self):
        _divWithPara = Element("div").add(Element("p"))
        _divWithPara._prettyIndent = True
        self.assertEqual(str(_divWithPara), '<div>\n  <p></p>\n</div>')
        
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

class ElementHtmlElementRoutingTestCase(ElementTestCase):
    def test_div_is_recognized(self):
        d = Element('div')
        self.assertNotEqual(type(d), Element) 
        from ..html.elements.div import Div
        self.assertIsInstance(d, Div)
        #Searches the chain assertNotIsInstance(d, Element)
    
class ElementConstructorTestCase(ElementTestCase):
    def setUp(self):
        self.div_with_span = Element('div', Element('span', Element('a')))
        #all tests rely on this 
        self.assertTrue(len(self.div_with_span._children))
        
    def test_first_child_is_span(self):
        self.assertEqual(self.div_with_span._children[0]._tagName, 'span')
        
    def test_first_child_level_2_is_a(self):
        self.assertTrue(len(self.div_with_span._children[0]._children))
        self.assertEqual(self.div_with_span._children[0]._children[0]._tagName, 'a')
        
    def test_kwargs_become_classes(self):
        _div_class = 'div-class'
        div_with_kwargs = Element('div', **{'class':'div-class'})
        self.assertIn(_div_class, div_with_kwargs._classes)
        
    def test_kwargs_become_data_attr(self):
        _div_data_attr = 'data-attr'
        _div_data_val = 'data-val'
        div_with_kwargs = Element('div', **{_div_data_attr:_div_data_val})
        self.assertIn(_div_data_attr, div_with_kwargs._attributes)
        self.assertEqual(div_with_kwargs._attributes[_div_data_attr], _div_data_val)
        
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
