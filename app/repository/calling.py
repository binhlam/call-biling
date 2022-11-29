# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger('call-billing')


class CallingRepository(object):
    def __init__(self, cr=None):
        self.cr = cr

    def lock(self, user_name):
        lock_sql = """
            SELECT call_count, block_count
            FROM call_billing
            WHERE user_name=%s
            FOR UPDATE;
        """
        data = None
        try:
            self.cr.execute(lock_sql, (user_name,))
            data = self.cr.fetchone()
        except Exception as e:
            _logger.error("[CallingRepository] lock error: %s" % str(e))

        return data

    def save(self, data):
        upsert_sql = """
            INSERT INTO call_billing (
                user_name,
                call_count,
                block_count,
                created_at
            )
            VALUES (
                %s,
                1,
                %s,
                now()
            )
            ON CONFLICT (user_name)
            DO UPDATE SET
                call_count = %s,
                block_count = %s,
                updated_at = now()
        """
        try:
            self.cr.execute(upsert_sql, (
                data.user_name, data.block_count, data.call_count, data.block_count, ))
        except Exception as e:
            _logger.error("[CallingRepository] record error: %s" % str(e))
            return False

        return True
