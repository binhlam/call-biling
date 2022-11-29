# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_cors import CORS
from .api.billing import BillingRequest
from .api.calling import CallingRequest

# Api blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def register_services(app):
    # Define endpoints
    api.add_resource(CallingRequest, '/<user_name>/call')
    api.add_resource(BillingRequest, '/<user_name>/billing')

    # # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/mobile')


def init_app():
    app = Flask("call-billing", static_url_path="")
    CORS(app, resources={r"/mobile/*": {"origins": "*"}})

    auth = HTTPBasicAuth()
    register_services(app)

    return app


flask_app = init_app()
