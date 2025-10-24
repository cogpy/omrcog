"""
Example demonstrating GraphQL queries with cogpy
"""

from cogpy.core import AtomSpace, TruthValue
from cogpy.graphql import create_app, schema
from cogpy.graphql.schema import set_atomspace


def setup_example_data():
    """Setup example data in AtomSpace"""
    atomspace = AtomSpace()
    
    # Create a simple knowledge graph about programming languages
    python = atomspace.add_node("ConceptNode", "Python")
    java = atomspace.add_node("ConceptNode", "Java")
    javascript = atomspace.add_node("ConceptNode", "JavaScript")
    language = atomspace.add_node("ConceptNode", "ProgrammingLanguage")
    
    # Add inheritance links
    atomspace.add_link("InheritanceLink", [python, language])
    atomspace.add_link("InheritanceLink", [java, language])
    atomspace.add_link("InheritanceLink", [javascript, language])
    
    # Add similarity links
    atomspace.add_link(
        "SimilarityLink",
        [python, javascript],
        TruthValue(strength=0.7, confidence=0.8)
    )
    
    return atomspace


def example_queries():
    """Run example GraphQL queries"""
    atomspace = setup_example_data()
    set_atomspace(atomspace)
    
    print("=" * 60)
    print("cogpy - GraphQL Query Examples")
    print("=" * 60)
    
    # Example 1: Get all nodes
    print("\n1. Query: Get all nodes")
    query1 = """
    {
        nodes {
            id
            type
            name
        }
    }
    """
    result1 = schema.execute(query1)
    print(f"   Found {len(result1.data['nodes'])} nodes:")
    for node in result1.data['nodes']:
        print(f"      - {node['name']} ({node['type']})")
    
    # Example 2: Get atoms by type
    print("\n2. Query: Get ConceptNodes")
    query2 = """
    {
        atomsByType(atomType: "ConceptNode") {
            ... on NodeType {
                name
                type
            }
        }
    }
    """
    result2 = schema.execute(query2)
    print(f"   Found {len(result2.data['atomsByType'])} ConceptNodes")
    
    # Example 3: Get all links
    print("\n3. Query: Get all links")
    query3 = """
    {
        links {
            type
            arity
        }
    }
    """
    result3 = schema.execute(query3)
    print(f"   Found {len(result3.data['links'])} links")
    for link in result3.data['links']:
        print(f"      - {link['type']} (arity: {link['arity']})")
    
    # Example 4: Add a new node via mutation
    print("\n4. Mutation: Add a new node")
    mutation = """
    mutation {
        addNode(atomType: "ConceptNode", name: "Ruby", strength: 1.0, confidence: 0.95) {
            node {
                name
                type
                truthValue {
                    strength
                    confidence
                }
            }
        }
    }
    """
    result4 = schema.execute(mutation)
    if result4.data:
        node_data = result4.data['addNode']['node']
        print(f"   Added: {node_data['name']}")
        print(f"   Truth value: strength={node_data['truthValue']['strength']}, "
              f"confidence={node_data['truthValue']['confidence']}")
    
    print("\n" + "=" * 60)
    print("GraphQL examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    example_queries()
