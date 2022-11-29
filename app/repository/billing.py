# -*- coding: utf-8 -*-
import psycopg2, psycopg2.extras
from pkg.db.database import _pool
import logging

_logger = logging.getLogger('call-billing')


class BillingRepository(object):
    def __init__(self, cr=None):
        self.cr = cr

    def fetch(self, user_name):
        fetch_sql = """
            SELECT
                block_count,
                call_count
            FROM call_billing
            WHERE user_name = %s
        """
        data = None
        try:
            self.cr.execute(fetch_sql, (user_name,))
            data = self.cr.fetchone()
        except Exception as e:
            _logger.error("[BillingRepository] fetch error: %s" % str(e))

        return data
