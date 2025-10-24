"""
Truth value representation for atoms
"""

from typing import Tuple


class TruthValue:
    """
    Represents a probabilistic truth value with strength and confidence.
    
    Attributes:
        strength: The strength of the truth value (0.0 to 1.0)
        confidence: The confidence in the truth value (0.0 to 1.0)
    """
    
    def __init__(self, strength: float = 1.0, confidence: float = 1.0):
        """
        Initialize a truth value.
        
        Args:
            strength: Truth strength (default: 1.0)
            confidence: Confidence level (default: 1.0)
        """
        self.strength = max(0.0, min(1.0, strength))
        self.confidence = max(0.0, min(1.0, confidence))
    
    def __repr__(self) -> str:
        return f"TruthValue(strength={self.strength:.3f}, confidence={self.confidence:.3f})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TruthValue):
            return False
        return (abs(self.strength - other.strength) < 1e-6 and
                abs(self.confidence - other.confidence) < 1e-6)
    
    def to_tuple(self) -> Tuple[float, float]:
        """Return truth value as a tuple (strength, confidence)"""
        return (self.strength, self.confidence)
    
    @classmethod
    def from_tuple(cls, values: Tuple[float, float]) -> "TruthValue":
        """Create TruthValue from tuple"""
        return cls(strength=values[0], confidence=values[1])
    
    def get_mean(self) -> float:
        """Get the mean truth value weighted by confidence"""
        return self.strength * self.confidence
