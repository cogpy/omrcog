# cogpy - OpenCog HyperGraphQL

A Python implementation of OpenCog's hypergraph-based knowledge representation with GraphQL query support.

## Overview

cogpy provides a lightweight, Python-native implementation of a hypergraph database inspired by OpenCog's AtomSpace, with GraphQL interfaces for querying and manipulating the knowledge graph.

## Features

- **HyperGraph Data Structures**: Atoms, Nodes, and Links for representing knowledge
- **AtomSpace**: In-memory hypergraph database
- **GraphQL API**: Query and manipulate the hypergraph using GraphQL
- **Type System**: Flexible type hierarchy for atoms
- **Truth Values**: Probabilistic truth values for uncertain reasoning

## Installation

```bash
cd cogpy
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
from cogpy.core import AtomSpace, Node, Link

# Create an AtomSpace
atomspace = AtomSpace()

# Add nodes
cat = atomspace.add_node("ConceptNode", "cat")
animal = atomspace.add_node("ConceptNode", "animal")

# Create a link
inheritance = atomspace.add_link("InheritanceLink", [cat, animal])

# Query atoms
atoms = atomspace.get_atoms_by_type("ConceptNode")
```

## GraphQL API

Run the GraphQL server:

```bash
python -m cogpy.graphql.server
```

Then query at `http://localhost:5000/graphql`:

```graphql
query {
  atoms {
    id
    type
    name
  }
}
```

## License

Same as Eclipse OMR project - EPL-2.0 OR Apache-2.0
