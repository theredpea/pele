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
        self.assertEqual(self.abcDiv._attributes['class'], 'a b c')
        

class NodeAddAttributeTestCase(NodeTestCase):
    def setUp(self):
        self.div = Node("div#idName#secondIdName")
        self.a = Node("a")

    def test_add_inserts(self):
        self.a.addAttribute("href", "http://www.google.com")
        self.assertIn("href", self.a._attributes)
        self.assertEqual(self.a._attributes["href"], "http://www.google.com")

        
        
    def test_attributes_override(self):
        self.assertIsNotNone(self.div._attributes['id'])
        self.assertEqual(self.div._attributes['id'],'secondIdName')
