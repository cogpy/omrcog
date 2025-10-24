"""
Flask server for the GraphQL API
"""

from flask import Flask, request, jsonify
from graphene import Schema

from cogpy.graphql.schema import schema, get_atomspace, set_atomspace
from cogpy.core import AtomSpace


def create_app(atomspace: AtomSpace = None) -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        atomspace: Optional AtomSpace instance to use
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Set the AtomSpace
    if atomspace:
        set_atomspace(atomspace)
    
    # Add GraphQL endpoint
    @app.route('/graphql', methods=['GET', 'POST'])
    def graphql_server():
        data = request.get_json() or {}
        query = data.get('query', '')
        variables = data.get('variables')
        operation_name = data.get('operationName')
        
        result = schema.execute(
            query,
            variables=variables,
            operation_name=operation_name
        )
        
        response = {}
        if result.data:
            response['data'] = result.data
        if result.errors:
            response['errors'] = [str(e) for e in result.errors]
        
        return jsonify(response)
    
    @app.route('/')
    def index():
        return """
        <html>
            <head><title>cogpy HyperGraphQL</title></head>
            <body>
                <h1>cogpy - HyperGraphQL Server</h1>
                <p>GraphQL endpoint: <a href="/graphql">/graphql</a></p>
                <p>Current AtomSpace size: {}</p>
                <p>Send POST requests to /graphql with JSON body containing "query" field</p>
            </body>
        </html>
        """.format(len(get_atomspace()))
    
    return app


def main():
    """Run the server"""
    app = create_app()
    print("Starting cogpy HyperGraphQL server...")
    print("GraphQL endpoint: http://localhost:5000/graphql")
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
