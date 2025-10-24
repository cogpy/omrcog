"""
Tests for TruthValue
"""

import unittest
from cogpy.core.truthvalue import TruthValue


class TestTruthValue(unittest.TestCase):
    """Test TruthValue class"""
    
    def test_default_values(self):
        """Test default truth values"""
        tv = TruthValue()
        self.assertEqual(tv.strength, 1.0)
        self.assertEqual(tv.confidence, 1.0)
    
    def test_custom_values(self):
        """Test custom truth values"""
        tv = TruthValue(0.8, 0.9)
        self.assertEqual(tv.strength, 0.8)
        self.assertEqual(tv.confidence, 0.9)
    
    def test_clamping(self):
        """Test values are clamped to [0, 1]"""
        tv1 = TruthValue(-0.5, 1.5)
        self.assertEqual(tv1.strength, 0.0)
        self.assertEqual(tv1.confidence, 1.0)
        
        tv2 = TruthValue(2.0, -1.0)
        self.assertEqual(tv2.strength, 1.0)
        self.assertEqual(tv2.confidence, 0.0)
    
    def test_to_tuple(self):
        """Test conversion to tuple"""
        tv = TruthValue(0.7, 0.8)
        self.assertEqual(tv.to_tuple(), (0.7, 0.8))
    
    def test_from_tuple(self):
        """Test creation from tuple"""
        tv = TruthValue.from_tuple((0.6, 0.7))
        self.assertEqual(tv.strength, 0.6)
        self.assertEqual(tv.confidence, 0.7)
    
    def test_get_mean(self):
        """Test mean calculation"""
        tv = TruthValue(0.8, 0.5)
        self.assertAlmostEqual(tv.get_mean(), 0.4)
    
    def test_equality(self):
        """Test equality comparison"""
        tv1 = TruthValue(0.8, 0.9)
        tv2 = TruthValue(0.8, 0.9)
        tv3 = TruthValue(0.7, 0.9)
        
        self.assertEqual(tv1, tv2)
        self.assertNotEqual(tv1, tv3)


if __name__ == '__main__':
    unittest.main()
