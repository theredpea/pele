import unittest
import timeit
from testElement import ElementTestCase
from html.modules.Module import Module


class ModuleTestCase(ElementTestCase):
    """Tests that classes are added"""
        
    def test_classes_added_for_modules_mro(self):
        module = Module()
       
        self.assertIn('Module', module.Container._classes)
        
    def test_classes_added_for_module_subclasses_mro(self):
        sub_module = SubModule()
        print(sub_module.Render())
        self.assertIn('SubModule', sub_module.Container._classes)
        sub_sub_module = SubSubModule()
        self.assertIn('SubSubModule', sub_sub_module.Container._classes)


class SubModule(Module):
    pass

class SubSubModule(SubModule):
    pass