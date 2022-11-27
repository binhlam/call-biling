# -*- coding: utf-8 -*-
#!flask/bin/python
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from app.controllers import api, api_bp, Calling, Billing


def init_app():
    app = Flask("call-billing", static_url_path="")
    auth = HTTPBasicAuth()

    # Define endpoints
    api.add_resource(Calling, '/<user_name>/call')
    api.add_resource(Billing, '/<user_name>/billing')

    # # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/mobile')

    return app


flask_app = init_app()
