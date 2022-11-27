# -*- coding: utf-8 -*-
from database import _pool
from configuration import _logger


class CallingRepository:

    @classmethod
    def record(cls, data):
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
        is_error = False
        try:
            with _pool.getconn() as conn:
                conn.cursor().execute(upsert_sql, (
                    data.user_name, data.block_count, data.call_count, data.block_count, ))
                conn.commit()

            _logger.info("[CallingRepository] Record success with user: %s" % data.user_name)
        except Exception as e:
            is_error = True
            _logger.error("[CallingRepository] Record error: %s" % str(e))
            conn.rollback()
        finally:
            _pool.putconn(conn)

        if is_error:
            return False

        return True
