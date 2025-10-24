# cogpy - OpenCog HyperGraphQL

A Python implementation of OpenCog's hypergraph-based knowledge representation with GraphQL query support.

## Overview

cogpy provides a lightweight, Python-native implementation of a hypergraph database inspired by OpenCog's AtomSpace, with GraphQL interfaces for querying and manipulating the knowledge graph.

## Features

- **HyperGraph Data Structures**: Atoms, Nodes, and Links for representing knowledge
- **AtomSpace**: In-memory hypergraph database with efficient indexing
- **Type System**: Flexible type hierarchy with 16+ atom types
- **Truth Values**: Probabilistic truth values for uncertain reasoning
- **GraphQL API**: Query and manipulate the hypergraph using GraphQL
- **Full CRUD Operations**: Add, remove, and query atoms
- **Comprehensive Tests**: 31+ unit tests ensuring reliability

## Installation

```bash
cd cogpy
pip install -r requirements.txt
pip install -e .
```

## Quick Start

### Python API

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
print(f"Found {len(atoms)} concepts")
```

### GraphQL Server

Run the GraphQL server:

```bash
cd examples
python run_server.py
```

Then query at `http://localhost:5000/graphql`:

```graphql
query {
  nodes {
    name
    type
  }
}
```

Or use curl:

```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ nodes { name type } }"}'
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[API.md](API.md)** - Complete API reference with examples
- **[examples/](examples/)** - Working code examples

## Atom Types

### Node Types
- `ConceptNode` - General concepts (e.g., "cat", "animal")
- `PredicateNode` - Predicates/properties (e.g., "runs", "eats")
- `VariableNode` - Variables for pattern matching
- `NumberNode` - Numeric values
- `SchemaNode` - Schemas/procedures

### Link Types
- `InheritanceLink` - Inheritance relationships (A is a B)
- `SimilarityLink` - Similarity relationships
- `ImplicationLink` - Logical implications
- `EvaluationLink` - Predicate evaluations
- `ListLink`, `SetLink` - Collections
- `AndLink`, `OrLink`, `NotLink` - Logical operators
- And more...

## Examples

### Basic Hypergraph Operations

```python
from cogpy.core import AtomSpace, TruthValue

atomspace = AtomSpace()

# Create a knowledge graph about animals
cat = atomspace.add_node("ConceptNode", "cat")
dog = atomspace.add_node("ConceptNode", "dog")
mammal = atomspace.add_node("ConceptNode", "mammal")

# Add relationships with truth values
atomspace.add_link("InheritanceLink", [cat, mammal], 
                   TruthValue(strength=1.0, confidence=1.0))
atomspace.add_link("SimilarityLink", [cat, dog],
                   TruthValue(strength=0.8, confidence=0.9))

# Query
incoming = atomspace.get_incoming(mammal)
print(f"Things that are mammals: {len(incoming)}")
```

### GraphQL Mutations

```graphql
mutation {
  addNode(
    atomType: "ConceptNode",
    name: "dog",
    strength: 1.0,
    confidence: 0.95
  ) {
    node {
      id
      name
      truthValue {
        strength
        confidence
      }
    }
  }
}
```

## Running Tests

```bash
cd /path/to/omrcog
PYTHONPATH=/path/to/omrcog python3 -m unittest discover cogpy/tests/ -v
```

All 31 tests should pass.

## Security

- CodeQL verified with 0 vulnerabilities
- Flask debug mode disabled by default
- Use `FLASK_DEBUG=true` environment variable only in development

## Architecture

```
cogpy/
├── core/              # Core hypergraph implementation
│   ├── atom.py        # Atom, Node, Link classes
│   ├── atomspace.py   # AtomSpace database
│   ├── types.py       # Type system
│   └── truthvalue.py  # Truth value implementation
├── graphql/           # GraphQL API
│   ├── schema.py      # GraphQL schema and resolvers
│   └── server.py      # Flask server
├── tests/             # Unit tests
├── examples/          # Usage examples
└── docs/              # Documentation
```

## License

Same as Eclipse OMR project - EPL-2.0 OR Apache-2.0

## Contributing

This is a demonstration implementation of OpenCog concepts with GraphQL support.
Contributions are welcome to extend functionality, add more atom types, or improve performance.
