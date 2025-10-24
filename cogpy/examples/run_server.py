#!/usr/bin/env python3
"""
Example showing how to run the cogpy GraphQL server
"""

import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cogpy.core import AtomSpace
from cogpy.graphql import create_app
from cogpy.graphql.schema import set_atomspace


def setup_demo_data():
    """Setup some demo data in the AtomSpace"""
    atomspace = AtomSpace()
    
    # Create some concepts
    ai = atomspace.add_node("ConceptNode", "ArtificialIntelligence")
    ml = atomspace.add_node("ConceptNode", "MachineLearning")
    dl = atomspace.add_node("ConceptNode", "DeepLearning")
    nlp = atomspace.add_node("ConceptNode", "NLP")
    cv = atomspace.add_node("ConceptNode", "ComputerVision")
    
    # Create relationships
    atomspace.add_link("InheritanceLink", [ml, ai])
    atomspace.add_link("InheritanceLink", [dl, ml])
    atomspace.add_link("InheritanceLink", [nlp, ml])
    atomspace.add_link("InheritanceLink", [cv, ml])
    
    return atomspace


if __name__ == '__main__':
    print("Setting up demo AtomSpace...")
    atomspace = setup_demo_data()
    print(f"Created {len(atomspace)} atoms")
    
    app = create_app(atomspace)
    
    print("\n" + "="*60)
    print("cogpy HyperGraphQL Server")
    print("="*60)
    print("\nServer starting at http://localhost:5000")
    print("GraphQL endpoint: http://localhost:5000/graphql")
    print("\nExample queries:")
    print("  - Get all nodes: { nodes { name type } }")
    print("  - Get all links: { links { type arity } }")
    print("\nSend POST requests with JSON body containing 'query' field")
    print("Set FLASK_DEBUG=true environment variable to enable debug mode")
    print("="*60 + "\n")
    
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
