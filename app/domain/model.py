# -*- coding: utf-8 -*-

class CallBillingModel(object):
    _columns = {
        'user_name': {'type': str, 'default': ''},
        'call_count': {'type': int, 'default': 0},
        'block_count': {'type': int, 'default': 0},
    }

    def __init__(self, dictionary):
        """Constructor"""
        for key in CallBillingModel._columns:
            val = dictionary.get(key, CallBillingModel._columns[key]['default'])
            if isinstance(key, str):
                key = key.strip()

            if isinstance(val, str):
                val = val.strip()

            setattr(self, key, val)
