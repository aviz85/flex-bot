# flex_app/__init__.py

from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    # ... rest of your app initialization
    return app

# Make sure to export create_app and db
__all__ = ['create_app']