import logging
from flask import Flask
from . import create_app  # import the factory from your app package

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    app.run(debug=False)