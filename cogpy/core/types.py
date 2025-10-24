"""
Atom type system for the hypergraph
"""

from enum import Enum
from typing import Set, Optional


class AtomType(Enum):
    """
    Enumeration of atom types in the hypergraph.
    Inspired by OpenCog's type hierarchy.
    """
    # Base types
    ATOM = "Atom"
    NODE = "Node"
    LINK = "Link"
    
    # Node types
    CONCEPT_NODE = "ConceptNode"
    PREDICATE_NODE = "PredicateNode"
    VARIABLE_NODE = "VariableNode"
    NUMBER_NODE = "NumberNode"
    SCHEMA_NODE = "SchemaNode"
    
    # Link types
    INHERITANCE_LINK = "InheritanceLink"
    SIMILARITY_LINK = "SimilarityLink"
    IMPLICATION_LINK = "ImplicationLink"
    EVALUATION_LINK = "EvaluationLink"
    EXECUTION_LINK = "ExecutionLink"
    LIST_LINK = "ListLink"
    SET_LINK = "SetLink"
    MEMBER_LINK = "MemberLink"
    AND_LINK = "AndLink"
    OR_LINK = "OrLink"
    NOT_LINK = "NotLink"
    
    @classmethod
    def is_node(cls, atom_type: "AtomType") -> bool:
        """Check if atom type is a node type"""
        node_types = {
            cls.NODE,
            cls.CONCEPT_NODE,
            cls.PREDICATE_NODE,
            cls.VARIABLE_NODE,
            cls.NUMBER_NODE,
            cls.SCHEMA_NODE,
        }
        return atom_type in node_types
    
    @classmethod
    def is_link(cls, atom_type: "AtomType") -> bool:
        """Check if atom type is a link type"""
        link_types = {
            cls.LINK,
            cls.INHERITANCE_LINK,
            cls.SIMILARITY_LINK,
            cls.IMPLICATION_LINK,
            cls.EVALUATION_LINK,
            cls.EXECUTION_LINK,
            cls.LIST_LINK,
            cls.SET_LINK,
            cls.MEMBER_LINK,
            cls.AND_LINK,
            cls.OR_LINK,
            cls.NOT_LINK,
        }
        return atom_type in link_types
    
    @classmethod
    def from_string(cls, type_str: str) -> "AtomType":
        """Convert string to AtomType"""
        for atom_type in cls:
            if atom_type.value == type_str:
                return atom_type
        raise ValueError(f"Unknown atom type: {type_str}")
