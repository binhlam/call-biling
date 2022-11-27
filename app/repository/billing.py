# -*- coding: utf-8 -*-
import psycopg2, psycopg2.extras
from database import _pool
from configuration import _logger


class BillingRepository:

    @classmethod
    def fetch(cls, user_name):
        fetch_sql = """
            SELECT
                block_count,
                call_count
            FROM call_billing
            WHERE user_name = %s
        """
        data = None
        try:
            with _pool.getconn() as conn:
                cr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cr.execute(fetch_sql, (user_name,))
                data = cr.fetchone()

            _logger.info("[BillingRepository] fetch success with user: %s" % user_name)
        except Exception as e:
            _logger.error("[BillingRepository] fetch error: %s" % str(e))
        finally:
            _pool.putconn(conn)

        return data
