import unittest
from Node import Node
import timeit

class NodeTestCase(unittest.TestCase):
    def setUp(self):
        self.div = Node("div#idName.className")


class NodeStringTestCase(NodeTestCase):
        
    def test_str_output_matches_string(self):
        self.assertEqual(str(self.div), '<div class="className" id="idName" ></div>')
        
    def test_str_output_matches_new_node_string(self):
        self.assertEqual(str(self.div), str(Node('div').addAttribute('id', 'idName').addAttribute('class','className')))
        
class NodeParseTagTestCase(NodeTestCase):
    def setUp(self):
        self.abcDiv = Node("div.a.b.c")
        
    def test_has_classes(self):
        self.assertIn('class', self.abcDiv._attributes)
        self.assertEqual(self.abcDiv._classes, set('abc'))
        
    def test_has_id(self):
        self.assertIn('class', self.abcDiv._attributes)
        self.assertEqual(self.abcDiv._classes, set('abc'))

class NodeAddTestCase(NodeTestCase):
        
    def test_number_children_equal_number_add(self):
        _num=3
        self.div.add([Node("p")]*_num)
        
        self.assertEqual(len(self.div.children), _num)

        
    def test_none_ignored(self):
        div = Node("div")
        _children = ['text', None, 'text']
        _truthyChildren = filter(None, _children)
        div.add(*_children)
        
        self.assertEqual(len(div.children), len(_truthyChildren))

        

        
class NodeAddAttributeTestCase(NodeTestCase):
    def setUp(self):
        self.a = Node("a")

    def test_add_inserts(self):
        self.a.addAttribute("href", "http://www.google.com")
        self.assertIn("href", self.a._attributes)
        self.assertEqual(self.a._attributes["href"], "http://www.google.com")

    def test_attributes_override(self):
        _1 = 'firstIdName'
        _2 = 'secondIdName'
        _3 = 'thirdIdName'
        
        self.div = Node('div#{0}#{1}'.format(_1, _2))
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
        div = Node('div#{}'.format(_i))
        self.assertEqual(div.id, _i)
        self.assertIsNotNone(div._attributes.get('id'))
        self.assertEqual(div.id, div._attributes.get('id'))
        
class NodeSpeedTestCase(NodeTestCase):
    
    class C(object):
            def __init__(self, **kwargs):
                    self.__dict__.update(kwargs)
                    
    def rowMaker(self, o):
        return Node("tr").append((Node("td").append(v) for k,v in sorted(o.__dict__.items())))
    
    def headerMaker(self, o):
        return Node("tr").append((Node("th").append(k) for k in sorted(o.__dict__.keys())))

    def test_timing_large_table(self):
        pass
