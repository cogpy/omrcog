# cogpy Quick Start Guide

## Installation

```bash
cd cogpy
pip install -r requirements.txt
pip install -e .
```

## Basic Usage (Python)

```python
from cogpy import AtomSpace, Node, Link, TruthValue

# Create an AtomSpace
atomspace = AtomSpace()

# Add some nodes
cat = atomspace.add_node("ConceptNode", "cat")
animal = atomspace.add_node("ConceptNode", "animal")

# Create a relationship
inheritance = atomspace.add_link("InheritanceLink", [cat, animal])

# Query the graph
all_concepts = atomspace.get_atoms_by_type("ConceptNode")
print(f"Found {len(all_concepts)} concepts")

# Get incoming links
incoming = atomspace.get_incoming(animal)
print(f"Links pointing to 'animal': {len(incoming)}")
```

## Running the GraphQL Server

```bash
cd cogpy/examples
python run_server.py
```

The server will start at `http://localhost:5000`

## Example GraphQL Queries

### Query all nodes
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ nodes { name type } }"}'
```

### Add a new node
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { addNode(atomType: \"ConceptNode\", name: \"dog\") { node { id name } } }"
  }'
```

## Running Tests

```bash
cd /path/to/omrcog
PYTHONPATH=/path/to/omrcog python3 -m unittest discover cogpy/tests/ -v
```

## Examples

See the `examples/` directory:
- `basic_example.py` - Demonstrates core hypergraph operations
- `graphql_example.py` - Shows GraphQL query capabilities
- `run_server.py` - Starts a GraphQL server with demo data

## Documentation

- `README.md` - Overview and features
- `API.md` - Complete API reference
- `QUICKSTART.md` - This file

## Environment Variables

- `FLASK_DEBUG=true` - Enable Flask debug mode (for development only)

## Security Note

Never run the server with `FLASK_DEBUG=true` in production environments.
