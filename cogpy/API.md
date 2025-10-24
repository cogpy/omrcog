# cogpy API Documentation

## Core Components

### AtomSpace

The central hypergraph database that stores and manages atoms.

```python
from cogpy.core import AtomSpace

# Create an AtomSpace
atomspace = AtomSpace()

# Check size
print(len(atomspace))  # Number of atoms
```

#### Methods

- `add_node(atom_type, name, truth_value=None)` - Add a node to the AtomSpace
- `add_link(atom_type, outgoing, truth_value=None)` - Add a link to the AtomSpace
- `remove_atom(atom)` - Remove an atom from the AtomSpace
- `get_atom_by_id(atom_id)` - Get an atom by its ID
- `get_atoms_by_type(atom_type)` - Get all atoms of a specific type
- `get_node_by_name(name, atom_type=None)` - Get a node by name
- `get_incoming(atom)` - Get all links that point to an atom
- `get_all_atoms()` - Get all atoms
- `get_all_nodes()` - Get all nodes
- `get_all_links()` - Get all links
- `clear()` - Remove all atoms

### Node

Represents a concept, predicate, or value in the hypergraph.

```python
from cogpy.core import Node, TruthValue

# Create a node
node = Node("ConceptNode", "cat")

# Create a node with truth value
node = Node("ConceptNode", "dog", TruthValue(0.9, 0.8))

# Access properties
print(node.name)  # "cat"
print(node.type)  # AtomType.CONCEPT_NODE
print(node.truth_value)  # TruthValue(...)
```

### Link

Represents a relationship between atoms in the hypergraph.

```python
from cogpy.core import Link, Node

# Create nodes
cat = Node("ConceptNode", "cat")
animal = Node("ConceptNode", "animal")

# Create a link
link = Link("InheritanceLink", [cat, animal])

# Access properties
print(link.type)  # AtomType.INHERITANCE_LINK
print(link.outgoing)  # [cat, animal]
print(link.get_arity())  # 2
```

### AtomType

Enumeration of supported atom types.

**Node Types:**
- `CONCEPT_NODE` - General concepts
- `PREDICATE_NODE` - Predicates/properties
- `VARIABLE_NODE` - Variables
- `NUMBER_NODE` - Numeric values
- `SCHEMA_NODE` - Schemas/procedures

**Link Types:**
- `INHERITANCE_LINK` - Inheritance relationships (A is a B)
- `SIMILARITY_LINK` - Similarity relationships
- `IMPLICATION_LINK` - Logical implications
- `EVALUATION_LINK` - Predicate evaluations
- `EXECUTION_LINK` - Procedure executions
- `LIST_LINK` - Ordered lists
- `SET_LINK` - Unordered sets
- `MEMBER_LINK` - Set membership
- `AND_LINK` - Logical AND
- `OR_LINK` - Logical OR
- `NOT_LINK` - Logical NOT

### TruthValue

Represents probabilistic truth values with strength and confidence.

```python
from cogpy.core import TruthValue

# Create truth value
tv = TruthValue(strength=0.8, confidence=0.9)

# Access properties
print(tv.strength)  # 0.8
print(tv.confidence)  # 0.9
print(tv.get_mean())  # 0.72 (strength * confidence)

# Convert to/from tuple
tuple_val = tv.to_tuple()  # (0.8, 0.9)
tv2 = TruthValue.from_tuple((0.7, 0.8))
```

## GraphQL API

### Starting the Server

```python
from cogpy.core import AtomSpace
from cogpy.graphql import create_app

atomspace = AtomSpace()
app = create_app(atomspace)
app.run(host='0.0.0.0', port=5000)
```

Or use the example server:
```bash
python cogpy/examples/run_server.py
```

### GraphQL Queries

#### Get All Nodes

```graphql
{
  nodes {
    id
    type
    name
    truthValue {
      strength
      confidence
    }
  }
}
```

#### Get All Links

```graphql
{
  links {
    id
    type
    arity
    outgoing {
      ... on NodeType {
        name
        type
      }
    }
  }
}
```

#### Get Atoms by Type

```graphql
{
  atomsByType(atomType: "ConceptNode") {
    ... on NodeType {
      name
      type
    }
  }
}
```

#### Get Node by Name

```graphql
{
  nodeByName(name: "cat", atomType: "ConceptNode") {
    id
    name
    type
  }
}
```

#### Get Incoming Links

```graphql
{
  incoming(atomId: "some-atom-id") {
    type
    arity
  }
}
```

### GraphQL Mutations

#### Add a Node

```graphql
mutation {
  addNode(
    atomType: "ConceptNode",
    name: "cat",
    strength: 1.0,
    confidence: 0.95
  ) {
    node {
      id
      name
      type
      truthValue {
        strength
        confidence
      }
    }
  }
}
```

#### Add a Link

```graphql
mutation {
  addLink(
    atomType: "InheritanceLink",
    outgoingIds: ["node-id-1", "node-id-2"],
    strength: 1.0,
    confidence: 1.0
  ) {
    link {
      id
      type
      arity
    }
  }
}
```

#### Remove an Atom

```graphql
mutation {
  removeAtom(atomId: "some-atom-id") {
    success
  }
}
```

### Example Python Usage with Requests

```python
import requests
import json

# Query
query = """
{
  nodes {
    name
    type
  }
}
"""

response = requests.post(
    'http://localhost:5000/graphql',
    json={'query': query}
)

data = response.json()
print(data)

# Mutation
mutation = """
mutation {
  addNode(atomType: "ConceptNode", name: "test") {
    node {
      id
      name
    }
  }
}
"""

response = requests.post(
    'http://localhost:5000/graphql',
    json={'query': mutation}
)

result = response.json()
print(result)
```

## Examples

See the `examples/` directory for complete working examples:

- `basic_example.py` - Core hypergraph operations
- `graphql_example.py` - GraphQL query examples
- `run_server.py` - Run the GraphQL server with demo data
