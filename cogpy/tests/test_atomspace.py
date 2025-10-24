"""
Tests for AtomSpace
"""

import unittest
from cogpy.core.atomspace import AtomSpace
from cogpy.core.atom import Node, Link
from cogpy.core.types import AtomType
from cogpy.core.truthvalue import TruthValue


class TestAtomSpace(unittest.TestCase):
    """Test AtomSpace class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.atomspace = AtomSpace()
    
    def test_create_atomspace(self):
        """Test creating an AtomSpace"""
        self.assertEqual(len(self.atomspace), 0)
    
    def test_add_node(self):
        """Test adding a node"""
        node = self.atomspace.add_node("ConceptNode", "cat")
        self.assertEqual(node.name, "cat")
        self.assertEqual(len(self.atomspace), 1)
    
    def test_add_duplicate_node(self):
        """Test adding duplicate nodes returns same node"""
        node1 = self.atomspace.add_node("ConceptNode", "cat")
        node2 = self.atomspace.add_node("ConceptNode", "cat")
        
        self.assertEqual(node1, node2)
        self.assertEqual(len(self.atomspace), 1)
    
    def test_add_link(self):
        """Test adding a link"""
        node1 = self.atomspace.add_node("ConceptNode", "cat")
        node2 = self.atomspace.add_node("ConceptNode", "animal")
        link = self.atomspace.add_link("InheritanceLink", [node1, node2])
        
        self.assertEqual(link.type, AtomType.INHERITANCE_LINK)
        self.assertEqual(len(self.atomspace), 3)  # 2 nodes + 1 link
    
    def test_get_atoms_by_type(self):
        """Test getting atoms by type"""
        self.atomspace.add_node("ConceptNode", "cat")
        self.atomspace.add_node("ConceptNode", "dog")
        self.atomspace.add_node("PredicateNode", "runs")
        
        concepts = self.atomspace.get_atoms_by_type("ConceptNode")
        self.assertEqual(len(concepts), 2)
        
        predicates = self.atomspace.get_atoms_by_type("PredicateNode")
        self.assertEqual(len(predicates), 1)
    
    def test_get_node_by_name(self):
        """Test getting node by name"""
        self.atomspace.add_node("ConceptNode", "cat")
        
        found = self.atomspace.get_node_by_name("cat")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "cat")
        
        not_found = self.atomspace.get_node_by_name("dog")
        self.assertIsNone(not_found)
    
    def test_get_incoming(self):
        """Test getting incoming links"""
        cat = self.atomspace.add_node("ConceptNode", "cat")
        dog = self.atomspace.add_node("ConceptNode", "dog")
        animal = self.atomspace.add_node("ConceptNode", "animal")
        
        self.atomspace.add_link("InheritanceLink", [cat, animal])
        self.atomspace.add_link("InheritanceLink", [dog, animal])
        
        incoming = self.atomspace.get_incoming(animal)
        self.assertEqual(len(incoming), 2)
    
    def test_remove_atom(self):
        """Test removing an atom"""
        node = self.atomspace.add_node("ConceptNode", "cat")
        self.assertEqual(len(self.atomspace), 1)
        
        success = self.atomspace.remove_atom(node)
        self.assertTrue(success)
        self.assertEqual(len(self.atomspace), 0)
    
    def test_remove_node_removes_incoming_links(self):
        """Test that removing a node also removes its incoming links"""
        cat = self.atomspace.add_node("ConceptNode", "cat")
        animal = self.atomspace.add_node("ConceptNode", "animal")
        self.atomspace.add_link("InheritanceLink", [cat, animal])
        
        self.assertEqual(len(self.atomspace), 3)
        
        self.atomspace.remove_atom(animal)
        self.assertEqual(len(self.atomspace), 1)  # Only cat remains
    
    def test_clear(self):
        """Test clearing the AtomSpace"""
        self.atomspace.add_node("ConceptNode", "cat")
        self.atomspace.add_node("ConceptNode", "dog")
        self.assertEqual(len(self.atomspace), 2)
        
        self.atomspace.clear()
        self.assertEqual(len(self.atomspace), 0)
    
    def test_get_all_nodes(self):
        """Test getting all nodes"""
        self.atomspace.add_node("ConceptNode", "cat")
        self.atomspace.add_node("ConceptNode", "dog")
        
        nodes = self.atomspace.get_all_nodes()
        self.assertEqual(len(nodes), 2)
    
    def test_get_all_links(self):
        """Test getting all links"""
        cat = self.atomspace.add_node("ConceptNode", "cat")
        dog = self.atomspace.add_node("ConceptNode", "dog")
        animal = self.atomspace.add_node("ConceptNode", "animal")
        
        self.atomspace.add_link("InheritanceLink", [cat, animal])
        self.atomspace.add_link("InheritanceLink", [dog, animal])
        
        links = self.atomspace.get_all_links()
        self.assertEqual(len(links), 2)


if __name__ == '__main__':
    unittest.main()
