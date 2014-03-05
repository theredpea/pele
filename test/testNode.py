import unittest
from Node import Node

class NodeStringTestCase(unittest.TestCase):
    def setUp(self):
        self.div = Node("div#idName.className")
        
    def runTest(self):
        self.assertEqual(str(self.div), '<div class="className" id="idName" ></div>')


class NodeAddAttributeTestCase(unittest.TestCase):
    def setUp(self):
        self.div = Node("div#idName#secondIdName")
        
    def runTest(self):
        self.assertIsNotNone(self.div._attributes['id'])
        self.assertEqual(self.div._attributes['id'],'secondIdName')
