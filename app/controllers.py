# -*- encoding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse
from app.service.calling import CallingService
from app.service.billing import BillingService
from jsonschema import validate, ValidationError, SchemaError
from configuration import _logger

# Api blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

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


class Calling(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('call_duration', type=int, required=True,
                        help='This field cannot be left blank')

    def put(self, user_name):
        def validate_request(req):
            try:
                validate(req, CALLING_SCHEMA)
            except ValidationError as e:
                return False, e.message
            except SchemaError as e:
                return False, e.message

            return True, None

        body = Calling.parser.parse_args()
        req_data = {
            'user_name': user_name,
            'call_duration': body.get('call_duration', 0)
        }
        _logger.info("[INFO] Record call with info: %s" % req_data)
        is_valid, err_mess = validate_request(req_data)
        if not is_valid:
            return jsonify({
                'is_success': 0,
                'error_message': err_mess,
            })

        is_success = CallingService.record(req_data)
        if not is_success:
            return jsonify({
                'is_success': 0,
                'error_message': "Error on recording user calling.",
            })

        return jsonify({
            'is_success': 1,
        })


class Billing(Resource):
    def get(self, user_name):
        def validate_request(req):
            try:
                validate(req, BILLING_SCHEMA)
            except ValidationError as e:
                return False, e.message
            except SchemaError as e:
                return False, e.message

            return True, None

        _logger.info("[INFO] Billing the call of user: %s" % user_name)
        is_valid, err_mess = validate_request({'user_name': user_name})
        if not is_valid:
            return jsonify({
                'is_success': 0,
                'error_message': err_mess,
            })

        record = BillingService.compute(user_name)
        if record is None:
            return jsonify({
                'is_success': 0,
                'error_message': "Cannot found data of user %s" % user_name,
            })

        return jsonify({
            "is_success": 1,
            "call_count": record.call_count,
            "block_count": record.block_count,
        })
