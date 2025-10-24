"""
Tests for Atom, Node, and Link classes
"""

import unittest
from cogpy.core.atom import Atom, Node, Link
from cogpy.core.types import AtomType
from cogpy.core.truthvalue import TruthValue


class TestNode(unittest.TestCase):
    """Test Node class"""
    
    def test_create_node(self):
        """Test creating a node"""
        node = Node(AtomType.CONCEPT_NODE, "cat")
        self.assertEqual(node.type, AtomType.CONCEPT_NODE)
        self.assertEqual(node.name, "cat")
        self.assertIsNotNone(node.id)
    
    def test_create_node_from_string(self):
        """Test creating node with string type"""
        node = Node("ConceptNode", "dog")
        self.assertEqual(node.type, AtomType.CONCEPT_NODE)
        self.assertEqual(node.name, "dog")
    
    def test_node_with_truth_value(self):
        """Test node with custom truth value"""
        tv = TruthValue(0.8, 0.9)
        node = Node(AtomType.CONCEPT_NODE, "cat", tv)
        self.assertEqual(node.truth_value, tv)
    
    def test_node_equality(self):
        """Test node equality"""
        node1 = Node(AtomType.CONCEPT_NODE, "cat")
        node2 = Node(AtomType.CONCEPT_NODE, "cat")
        node3 = Node(AtomType.CONCEPT_NODE, "dog")
        
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)


class TestLink(unittest.TestCase):
    """Test Link class"""
    
    def test_create_link(self):
        """Test creating a link"""
        node1 = Node(AtomType.CONCEPT_NODE, "cat")
        node2 = Node(AtomType.CONCEPT_NODE, "animal")
        link = Link(AtomType.INHERITANCE_LINK, [node1, node2])
        
        self.assertEqual(link.type, AtomType.INHERITANCE_LINK)
        self.assertEqual(len(link.outgoing), 2)
        self.assertEqual(link.outgoing[0], node1)
        self.assertEqual(link.outgoing[1], node2)
    
    def test_create_link_from_string(self):
        """Test creating link with string type"""
        node1 = Node(AtomType.CONCEPT_NODE, "cat")
        node2 = Node(AtomType.CONCEPT_NODE, "animal")
        link = Link("InheritanceLink", [node1, node2])
        
        self.assertEqual(link.type, AtomType.INHERITANCE_LINK)
    
    def test_link_arity(self):
        """Test link arity"""
        node1 = Node(AtomType.CONCEPT_NODE, "a")
        node2 = Node(AtomType.CONCEPT_NODE, "b")
        node3 = Node(AtomType.CONCEPT_NODE, "c")
        
        link = Link(AtomType.LIST_LINK, [node1, node2, node3])
        self.assertEqual(link.get_arity(), 3)
    
    def test_link_equality(self):
        """Test link equality"""
        node1 = Node(AtomType.CONCEPT_NODE, "cat")
        node2 = Node(AtomType.CONCEPT_NODE, "animal")
        
        link1 = Link(AtomType.INHERITANCE_LINK, [node1, node2])
        link2 = Link(AtomType.INHERITANCE_LINK, [node1, node2])
        link3 = Link(AtomType.SIMILARITY_LINK, [node1, node2])
        
        self.assertEqual(link1, link2)
        self.assertNotEqual(link1, link3)


if __name__ == '__main__':
    unittest.main()
