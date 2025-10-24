"""
AtomSpace - the hypergraph database
"""

from typing import List, Optional, Set, Union, Dict
from collections import defaultdict

from cogpy.core.atom import Atom, Node, Link
from cogpy.core.types import AtomType
from cogpy.core.truthvalue import TruthValue


class AtomSpace:
    """
    The AtomSpace is the central hypergraph database.
    It stores and manages atoms (nodes and links) and provides
    methods for adding, removing, and querying atoms.
    """
    
    def __init__(self):
        """Initialize an empty AtomSpace"""
        self._atoms: Dict[str, Atom] = {}  # id -> atom
        self._nodes_by_type: Dict[AtomType, Set[Node]] = defaultdict(set)
        self._nodes_by_name: Dict[str, Set[Node]] = defaultdict(set)
        self._links_by_type: Dict[AtomType, Set[Link]] = defaultdict(set)
        self._incoming: Dict[str, Set[Link]] = defaultdict(set)  # atom_id -> links pointing to it
    
    def add_node(
        self,
        atom_type: Union[AtomType, str],
        name: str,
        truth_value: Optional[TruthValue] = None,
    ) -> Node:
        """
        Add a node to the AtomSpace.
        
        Args:
            atom_type: Type of the node
            name: Name of the node
            truth_value: Optional truth value
            
        Returns:
            The created or existing node
        """
        if isinstance(atom_type, str):
            atom_type = AtomType.from_string(atom_type)
        
        # Check if node already exists
        for node in self._nodes_by_name.get(name, set()):
            if node.type == atom_type:
                # Update truth value if provided
                if truth_value:
                    node.truth_value = truth_value
                return node
        
        # Create new node
        node = Node(atom_type, name, truth_value)
        self._atoms[node.id] = node
        self._nodes_by_type[atom_type].add(node)
        self._nodes_by_name[name].add(node)
        
        return node
    
    def add_link(
        self,
        atom_type: Union[AtomType, str],
        outgoing: List[Atom],
        truth_value: Optional[TruthValue] = None,
    ) -> Link:
        """
        Add a link to the AtomSpace.
        
        Args:
            atom_type: Type of the link
            outgoing: List of atoms the link connects
            truth_value: Optional truth value
            
        Returns:
            The created or existing link
        """
        if isinstance(atom_type, str):
            atom_type = AtomType.from_string(atom_type)
        
        # Check if link already exists
        for link in self._links_by_type.get(atom_type, set()):
            if link.outgoing == outgoing:
                # Update truth value if provided
                if truth_value:
                    link.truth_value = truth_value
                return link
        
        # Create new link
        link = Link(atom_type, outgoing, truth_value)
        self._atoms[link.id] = link
        self._links_by_type[atom_type].add(link)
        
        # Update incoming sets
        for atom in outgoing:
            self._incoming[atom.id].add(link)
        
        return link
    
    def remove_atom(self, atom: Atom) -> bool:
        """
        Remove an atom from the AtomSpace.
        
        Args:
            atom: The atom to remove
            
        Returns:
            True if removed, False if not found
        """
        if atom.id not in self._atoms:
            return False
        
        # Remove from main storage
        del self._atoms[atom.id]
        
        if isinstance(atom, Node):
            # Remove from node indices
            self._nodes_by_type[atom.type].discard(atom)
            self._nodes_by_name[atom.name].discard(atom)
            
            # Remove all incoming links
            for link in list(self._incoming.get(atom.id, set())):
                self.remove_atom(link)
        
        elif isinstance(atom, Link):
            # Remove from link indices
            self._links_by_type[atom.type].discard(atom)
            
            # Remove from incoming sets
            for out_atom in atom.outgoing:
                self._incoming[out_atom.id].discard(atom)
        
        # Clean up incoming
        if atom.id in self._incoming:
            del self._incoming[atom.id]
        
        return True
    
    def get_atom_by_id(self, atom_id: str) -> Optional[Atom]:
        """Get an atom by its ID"""
        return self._atoms.get(atom_id)
    
    def get_atoms_by_type(self, atom_type: Union[AtomType, str]) -> List[Atom]:
        """
        Get all atoms of a specific type.
        
        Args:
            atom_type: Type to filter by
            
        Returns:
            List of atoms of the specified type
        """
        if isinstance(atom_type, str):
            atom_type = AtomType.from_string(atom_type)
        
        if AtomType.is_node(atom_type):
            return list(self._nodes_by_type.get(atom_type, set()))
        else:
            return list(self._links_by_type.get(atom_type, set()))
    
    def get_node_by_name(self, name: str, atom_type: Optional[Union[AtomType, str]] = None) -> Optional[Node]:
        """
        Get a node by name and optionally type.
        
        Args:
            name: Name of the node
            atom_type: Optional type filter
            
        Returns:
            The node if found, None otherwise
        """
        nodes = self._nodes_by_name.get(name, set())
        
        if atom_type:
            if isinstance(atom_type, str):
                atom_type = AtomType.from_string(atom_type)
            
            for node in nodes:
                if node.type == atom_type:
                    return node
            return None
        
        return next(iter(nodes), None) if nodes else None
    
    def get_incoming(self, atom: Atom) -> List[Link]:
        """
        Get all links that point to this atom.
        
        Args:
            atom: The target atom
            
        Returns:
            List of incoming links
        """
        return list(self._incoming.get(atom.id, set()))
    
    def get_all_atoms(self) -> List[Atom]:
        """Get all atoms in the AtomSpace"""
        return list(self._atoms.values())
    
    def get_all_nodes(self) -> List[Node]:
        """Get all nodes in the AtomSpace"""
        return [atom for atom in self._atoms.values() if isinstance(atom, Node)]
    
    def get_all_links(self) -> List[Link]:
        """Get all links in the AtomSpace"""
        return [atom for atom in self._atoms.values() if isinstance(atom, Link)]
    
    def clear(self):
        """Remove all atoms from the AtomSpace"""
        self._atoms.clear()
        self._nodes_by_type.clear()
        self._nodes_by_name.clear()
        self._links_by_type.clear()
        self._incoming.clear()
    
    def __len__(self) -> int:
        """Return the number of atoms in the AtomSpace"""
        return len(self._atoms)
    
    def __repr__(self) -> str:
        return f"AtomSpace(atoms={len(self._atoms)})"
