#!/usr/bin/env python3

"""
Boilerplate Flask setup for service application (should not be modified)
"""

from flask import Flask
from flask_graphql import GraphQLView
from .schema import schema


def create_app():
    """
    Creates graphql and graphiql endpoints
    """

    app = Flask(__name__)
    app.debug = True

    app.add_url_rule(
        '/',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=False
        )
    )

    app.add_url_rule(
        '/graphiql',
        view_func=GraphQLView.as_view(
            'graphiql',
            schema=schema,
            graphiql=True
        )
    )

    return app
