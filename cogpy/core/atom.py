"""
Atom classes for the hypergraph
"""

from typing import List, Optional, Union
from uuid import uuid4

from cogpy.core.types import AtomType
from cogpy.core.truthvalue import TruthValue


class Atom:
    """
    Base class for all atoms in the hypergraph.
    An atom represents a node or link in the knowledge graph.
    """
    
    def __init__(
        self,
        atom_type: Union[AtomType, str],
        truth_value: Optional[TruthValue] = None,
    ):
        """
        Initialize an atom.
        
        Args:
            atom_type: Type of the atom
            truth_value: Optional truth value for the atom
        """
        if isinstance(atom_type, str):
            atom_type = AtomType.from_string(atom_type)
        
        self.id = str(uuid4())
        self.type = atom_type
        self.truth_value = truth_value or TruthValue()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, type={self.type.value})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Atom):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)


class Node(Atom):
    """
    A node in the hypergraph with a name.
    Nodes represent concepts, predicates, or values.
    """
    
    def __init__(
        self,
        atom_type: Union[AtomType, str],
        name: str,
        truth_value: Optional[TruthValue] = None,
    ):
        """
        Initialize a node.
        
        Args:
            atom_type: Type of the node
            name: Name of the node
            truth_value: Optional truth value
        """
        super().__init__(atom_type, truth_value)
        self.name = name
    
    def __repr__(self) -> str:
        return f"Node(type={self.type.value}, name='{self.name}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self.type == other.type and self.name == other.name
    
    def __hash__(self) -> int:
        return hash((self.type, self.name))


class Link(Atom):
    """
    A link in the hypergraph connecting multiple atoms.
    Links represent relationships between atoms.
    """
    
    def __init__(
        self,
        atom_type: Union[AtomType, str],
        outgoing: List[Atom],
        truth_value: Optional[TruthValue] = None,
    ):
        """
        Initialize a link.
        
        Args:
            atom_type: Type of the link
            outgoing: List of atoms this link connects
            truth_value: Optional truth value
        """
        super().__init__(atom_type, truth_value)
        self.outgoing = outgoing if outgoing else []
    
    def __repr__(self) -> str:
        outgoing_str = ", ".join([str(atom) for atom in self.outgoing])
        return f"Link(type={self.type.value}, outgoing=[{outgoing_str}])"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Link):
            return False
        return (self.type == other.type and
                len(self.outgoing) == len(other.outgoing) and
                all(a == b for a, b in zip(self.outgoing, other.outgoing)))
    
    def __hash__(self) -> int:
        return hash((self.type, tuple(self.outgoing)))
    
    def get_arity(self) -> int:
        """Get the number of outgoing atoms"""
        return len(self.outgoing)
