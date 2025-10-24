"""
GraphQL module for querying the hypergraph
"""

from cogpy.graphql.schema import schema
from cogpy.graphql.server import create_app

__all__ = [
    "schema",
    "create_app",
]
