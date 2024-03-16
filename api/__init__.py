from flask import Flask
from . import syringe_routes
from . import microscope_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(syringe_routes.api, url_prefix="/api")
    app.register_blueprint(microscope_routes.api, url_prefix="/api")
    return app