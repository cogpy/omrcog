"""
GraphQL schema for the hypergraph
"""

import graphene
from typing import Optional, List as TypeList

from cogpy.core import AtomSpace, Atom, Node, Link, AtomType


# Global AtomSpace instance for the GraphQL API
_atomspace = AtomSpace()


def get_atomspace() -> AtomSpace:
    """Get the global AtomSpace instance"""
    return _atomspace


def set_atomspace(atomspace: AtomSpace):
    """Set the global AtomSpace instance"""
    global _atomspace
    _atomspace = atomspace


class TruthValueType(graphene.ObjectType):
    """GraphQL type for TruthValue"""
    strength = graphene.Float()
    confidence = graphene.Float()


class AtomInterface(graphene.Interface):
    """GraphQL interface for all atoms"""
    id = graphene.String()
    type = graphene.String()
    truth_value = graphene.Field(TruthValueType)


class NodeType(graphene.ObjectType):
    """GraphQL type for Node"""
    class Meta:
        interfaces = (AtomInterface,)
    
    name = graphene.String()
    
    def resolve_id(self, info):
        return self.id
    
    def resolve_type(self, info):
        return self.type.value if hasattr(self.type, 'value') else str(self.type)
    
    def resolve_truth_value(self, info):
        return self.truth_value
    
    def resolve_name(self, info):
        return self.name


class LinkType(graphene.ObjectType):
    """GraphQL type for Link"""
    class Meta:
        interfaces = (AtomInterface,)
    
    outgoing = graphene.List(lambda: AtomUnion)
    arity = graphene.Int()
    
    def resolve_id(self, info):
        return self.id
    
    def resolve_type(self, info):
        return self.type.value if hasattr(self.type, 'value') else str(self.type)
    
    def resolve_truth_value(self, info):
        return self.truth_value
    
    def resolve_outgoing(self, info):
        return self.outgoing
    
    def resolve_arity(self, info):
        return self.get_arity()


class AtomUnion(graphene.Union):
    """Union type for Atom (can be Node or Link)"""
    class Meta:
        types = (NodeType, LinkType)


class Query(graphene.ObjectType):
    """GraphQL queries for the hypergraph"""
    
    # Get all atoms
    atoms = graphene.List(AtomUnion)
    
    # Get all nodes
    nodes = graphene.List(NodeType)
    
    # Get all links
    links = graphene.List(LinkType)
    
    # Get atom by ID
    atom_by_id = graphene.Field(AtomUnion, id=graphene.String(required=True))
    
    # Get atoms by type
    atoms_by_type = graphene.List(AtomUnion, atom_type=graphene.String(required=True))
    
    # Get node by name
    node_by_name = graphene.Field(
        NodeType,
        name=graphene.String(required=True),
        atom_type=graphene.String()
    )
    
    # Get incoming links for an atom
    incoming = graphene.List(LinkType, atom_id=graphene.String(required=True))
    
    def resolve_atoms(self, info):
        """Resolve all atoms"""
        atomspace = get_atomspace()
        return atomspace.get_all_atoms()
    
    def resolve_nodes(self, info):
        """Resolve all nodes"""
        atomspace = get_atomspace()
        return atomspace.get_all_nodes()
    
    def resolve_links(self, info):
        """Resolve all links"""
        atomspace = get_atomspace()
        return atomspace.get_all_links()
    
    def resolve_atom_by_id(self, info, id):
        """Resolve atom by ID"""
        atomspace = get_atomspace()
        return atomspace.get_atom_by_id(id)
    
    def resolve_atoms_by_type(self, info, atom_type):
        """Resolve atoms by type"""
        atomspace = get_atomspace()
        return atomspace.get_atoms_by_type(atom_type)
    
    def resolve_node_by_name(self, info, name, atom_type=None):
        """Resolve node by name"""
        atomspace = get_atomspace()
        return atomspace.get_node_by_name(name, atom_type)
    
    def resolve_incoming(self, info, atom_id):
        """Resolve incoming links for an atom"""
        atomspace = get_atomspace()
        atom = atomspace.get_atom_by_id(atom_id)
        if atom:
            return atomspace.get_incoming(atom)
        return []


class AddNodeMutation(graphene.Mutation):
    """Mutation to add a node to the AtomSpace"""
    class Arguments:
        atom_type = graphene.String(required=True)
        name = graphene.String(required=True)
        strength = graphene.Float(default_value=1.0)
        confidence = graphene.Float(default_value=1.0)
    
    node = graphene.Field(NodeType)
    
    def mutate(self, info, atom_type, name, strength=1.0, confidence=1.0):
        from cogpy.core.truthvalue import TruthValue
        
        atomspace = get_atomspace()
        tv = TruthValue(strength, confidence)
        node = atomspace.add_node(atom_type, name, tv)
        return AddNodeMutation(node=node)


class AddLinkMutation(graphene.Mutation):
    """Mutation to add a link to the AtomSpace"""
    class Arguments:
        atom_type = graphene.String(required=True)
        outgoing_ids = graphene.List(graphene.String, required=True)
        strength = graphene.Float(default_value=1.0)
        confidence = graphene.Float(default_value=1.0)
    
    link = graphene.Field(LinkType)
    
    def mutate(self, info, atom_type, outgoing_ids, strength=1.0, confidence=1.0):
        from cogpy.core.truthvalue import TruthValue
        
        atomspace = get_atomspace()
        
        # Get outgoing atoms
        outgoing = []
        for atom_id in outgoing_ids:
            atom = atomspace.get_atom_by_id(atom_id)
            if atom:
                outgoing.append(atom)
        
        if len(outgoing) != len(outgoing_ids):
            raise ValueError("Some atoms not found")
        
        tv = TruthValue(strength, confidence)
        link = atomspace.add_link(atom_type, outgoing, tv)
        return AddLinkMutation(link=link)


class RemoveAtomMutation(graphene.Mutation):
    """Mutation to remove an atom from the AtomSpace"""
    class Arguments:
        atom_id = graphene.String(required=True)
    
    success = graphene.Boolean()
    
    def mutate(self, info, atom_id):
        atomspace = get_atomspace()
        atom = atomspace.get_atom_by_id(atom_id)
        if atom:
            success = atomspace.remove_atom(atom)
            return RemoveAtomMutation(success=success)
        return RemoveAtomMutation(success=False)


class Mutation(graphene.ObjectType):
    """GraphQL mutations for the hypergraph"""
    add_node = AddNodeMutation.Field()
    add_link = AddLinkMutation.Field()
    remove_atom = RemoveAtomMutation.Field()


# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
