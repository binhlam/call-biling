# -*- encoding: utf-8 -*-
from flask import jsonify, make_response
from app.service.billing import BillingService
from pkg.rest.response import response_error, response_success
from pkg.rest.response import CODE_OK, CODE_ERR
from pkg.rest.request import BaseValidation
from flask_restful import Resource, reqparse
import logging

_logger = logging.getLogger('call-billing')

# schema
BILLING_SCHEMA = {
    'type': 'object',
    'required': ['user_name'],
    'properties': {
        'user_name': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 32,
        }
    }
}


class BillingRequest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_name', type=str, required=True,
                                 help='This field cannot be left blank',
                                 location='args')
        super(BillingRequest, self).__init__()

    def get(self, user_name):
        req_data = {
            'user_name': user_name
        }
        _logger.info("GET request - payload: %s" % req_data)

        is_valid, err_mess = BaseValidation.validate_schema(req_data, BILLING_SCHEMA)
        if not is_valid:
            return make_response(
                jsonify(response_error(err_mess)), CODE_ERR)

        service = BillingService()
        record = service.fetch(user_name)
        if record is None:
            err_mess = "Cannot found data of user %s" % user_name
            return make_response(
                jsonify(response_error(err_mess)), CODE_ERR)

        return make_response(
            jsonify(response_success(record)), CODE_OK)
