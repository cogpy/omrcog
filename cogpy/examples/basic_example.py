"""
Basic example demonstrating cogpy hypergraph usage
"""

from cogpy.core import AtomSpace, Node, Link, AtomType, TruthValue


def main():
    """Run basic example"""
    print("=" * 60)
    print("cogpy - OpenCog HyperGraph Example")
    print("=" * 60)
    
    # Create an AtomSpace
    atomspace = AtomSpace()
    print(f"\nCreated AtomSpace: {atomspace}")
    
    # Create some concept nodes
    print("\n1. Adding concept nodes...")
    cat = atomspace.add_node("ConceptNode", "cat")
    dog = atomspace.add_node("ConceptNode", "dog")
    animal = atomspace.add_node("ConceptNode", "animal")
    mammal = atomspace.add_node("ConceptNode", "mammal")
    
    print(f"   - {cat}")
    print(f"   - {dog}")
    print(f"   - {animal}")
    print(f"   - {mammal}")
    
    # Create inheritance links
    print("\n2. Adding inheritance links...")
    cat_is_mammal = atomspace.add_link(
        "InheritanceLink",
        [cat, mammal],
        TruthValue(strength=1.0, confidence=1.0)
    )
    dog_is_mammal = atomspace.add_link(
        "InheritanceLink",
        [dog, mammal],
        TruthValue(strength=1.0, confidence=1.0)
    )
    mammal_is_animal = atomspace.add_link(
        "InheritanceLink",
        [mammal, animal],
        TruthValue(strength=1.0, confidence=0.99)
    )
    
    print(f"   - {cat_is_mammal}")
    print(f"   - {dog_is_mammal}")
    print(f"   - {mammal_is_animal}")
    
    # Create a similarity link
    print("\n3. Adding similarity link...")
    cat_similar_dog = atomspace.add_link(
        "SimilarityLink",
        [cat, dog],
        TruthValue(strength=0.8, confidence=0.9)
    )
    print(f"   - {cat_similar_dog}")
    
    # Query atoms
    print("\n4. Querying atoms...")
    concepts = atomspace.get_atoms_by_type("ConceptNode")
    print(f"   Concept nodes: {len(concepts)}")
    for concept in concepts:
        print(f"      - {concept.name}")
    
    inheritance_links = atomspace.get_atoms_by_type("InheritanceLink")
    print(f"   Inheritance links: {len(inheritance_links)}")
    
    # Get incoming links
    print("\n5. Getting incoming links for 'mammal'...")
    incoming = atomspace.get_incoming(mammal)
    print(f"   Found {len(incoming)} incoming links:")
    for link in incoming:
        print(f"      - {link.type.value}: {[a.name for a in link.outgoing if isinstance(a, Node)]}")
    
    # Get node by name
    print("\n6. Looking up node by name...")
    found_cat = atomspace.get_node_by_name("cat", "ConceptNode")
    print(f"   Found: {found_cat}")
    print(f"   Truth value: {found_cat.truth_value}")
    
    # Statistics
    print("\n7. AtomSpace statistics:")
    print(f"   Total atoms: {len(atomspace)}")
    print(f"   Nodes: {len(atomspace.get_all_nodes())}")
    print(f"   Links: {len(atomspace.get_all_links())}")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
