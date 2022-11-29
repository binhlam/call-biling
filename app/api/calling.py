# -*- encoding: utf-8 -*-
from flask import jsonify, make_response
from app.service.calling import CallingService
from pkg.rest.response import response_error, response_success
from pkg.rest.response import CODE_OK, CODE_ERR
from pkg.rest.request import BaseValidation
from flask_restful import Resource, reqparse
import logging

_logger = logging.getLogger('call-billing')

# schema
CALLING_SCHEMA = {
    'type': 'object',
    'required': ['user_name', 'call_duration'],
    'properties': {
        'user_name': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 32,
        },
        'call_duration': {
            'type': 'number',
            'minimum': 1,
        }
    }
}


class CallingRequest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('call_duration', type=int, required=True,
                                 help='This field cannot be left blank',
                                 location='json')
        super(CallingRequest, self).__init__()

    def put(self, user_name):
        body = self.parser.parse_args()
        req_data = {
            'user_name': user_name,
            'call_duration': body.get('call_duration', 0)
        }
        _logger.info("[CALLING] put request - payload: %s" % req_data)

        is_valid, err_mess = BaseValidation.validate_schema(req_data, CALLING_SCHEMA)
        if not is_valid:
            return make_response(
                jsonify(response_error(err_mess)), CODE_ERR)

        service = CallingService()
        is_success = service.record(req_data)
        if not is_success:
            err_mess = "Error on recording user calling."
            return make_response(
                jsonify(response_error(err_mess)), CODE_ERR)

        return make_response(
            jsonify(response_success()), CODE_OK)
