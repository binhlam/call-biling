# -*- coding: utf-8 -*-
from app.repository.billing import BillingRepository
from pkg.db.database import _pool
import psycopg2, psycopg2.extras
import logging

_logger = logging.getLogger('call-billing')


class BillingService(object):

    def fetch(self, user_name):
        """
        Function get billing by user_name
        :param user_name:
        :return: data
        """
        try:
            with _pool.getconn() as conn:
                cr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                repo = BillingRepository(cr=cr)
                record = repo.fetch(user_name)

            _logger.info("[BillingRepository] fetch success with user: %s" % user_name)
        finally:
            _pool.putconn(conn)

        return record
