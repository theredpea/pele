import unittest
from Node import Node

class NodeTestCase(unittest.TestCase):
    def setUp(self):
        self.div = Node("div#idName.className")


class NodeStringTestCase(NodeTestCase):
        
    def test_str_1(self):
        self.assertEqual(str(self.div), '<div class="className" id="idName" ></div>')


class NodeConstructorTestCase(NodeTestCase):
        
    def test_same_as_(self):
        self.assertEqual(str(self.div), str(Node('div').addAttribute('id', 'idName').addAttribute('class','className')))
        
class NodeParseTagTestCase(NodeTestCase):
    def setUp(self):
        self.abcDiv = Node("div.a.b.c")
        
    def test_multiple_classes(self):
        self.assertIn('class', self.abcDiv._attributes)
        self.assertEqual(self.abcDiv._classes, set('abc'))
        

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
        


    
