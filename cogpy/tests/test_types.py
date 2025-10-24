"""
Tests for atom types
"""

import unittest
from cogpy.core.types import AtomType


class TestAtomType(unittest.TestCase):
    """Test AtomType enumeration"""
    
    def test_from_string(self):
        """Test converting string to AtomType"""
        self.assertEqual(AtomType.from_string("ConceptNode"), AtomType.CONCEPT_NODE)
        self.assertEqual(AtomType.from_string("InheritanceLink"), AtomType.INHERITANCE_LINK)
    
    def test_from_string_invalid(self):
        """Test invalid string raises ValueError"""
        with self.assertRaises(ValueError):
            AtomType.from_string("InvalidType")
    
    def test_is_node(self):
        """Test is_node classification"""
        self.assertTrue(AtomType.is_node(AtomType.NODE))
        self.assertTrue(AtomType.is_node(AtomType.CONCEPT_NODE))
        self.assertFalse(AtomType.is_node(AtomType.LINK))
        self.assertFalse(AtomType.is_node(AtomType.INHERITANCE_LINK))
    
    def test_is_link(self):
        """Test is_link classification"""
        self.assertTrue(AtomType.is_link(AtomType.LINK))
        self.assertTrue(AtomType.is_link(AtomType.INHERITANCE_LINK))
        self.assertFalse(AtomType.is_link(AtomType.NODE))
        self.assertFalse(AtomType.is_link(AtomType.CONCEPT_NODE))


if __name__ == '__main__':
    unittest.main()
