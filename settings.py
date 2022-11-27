# -*- coding: utf-8 -*-
import os

# file path
base_path = os.path.dirname(__file__)
app_api_path = '{}/{}'.format(base_path, 'call-billing/app/__init__.py')
FLASK_APP = os.environ.get('FLASK_APP', app_api_path)
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'call_billing')
DB_USER = os.environ.get('DB_USER', 'binhlam')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'binhlam')
DB_MINCONN = int(os.environ.get('DB_MINCONN', 16))
DB_MAXCONN = int(os.environ.get('DB_MAXCONN', 64))

# SET ENV VAR FOR LATER ACCESS
__ENV_VARIABLES__ = {
    'FLASK_APP': FLASK_APP,
    'FLASK_ENV': FLASK_ENV,
    'DB_HOST': DB_HOST,
    'DB_NAME': DB_NAME,
    'DB_PASSWORD': DB_PASSWORD,
    'DB_USER': DB_USER,
    'DB_MAXCONN': DB_MAXCONN,
    'DB_MINCONN': DB_MINCONN,
    'DB_PORT': DB_PORT,
}
