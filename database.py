# -*- encoding: utf-8 -*-
from psycopg2.pool import ThreadedConnectionPool
import logging

_logger = logging.getLogger('call-billing')
_pool = None


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls.__instances:
            raise "Cannot initialize this class twice."

        instance = super().__call__(*args, **kwargs)
        cls.__instances[cls] = instance
        return instance


class ConnectionPool(metaclass=Singleton):
    def __init__(self):
        super(ConnectionPool, self).__init__()

    def init_pool(self, config):
        global _pool
        try:
            _logger.info("[DB] Connecting to DB, this may take a while due to latency issue....")
            _pool = ThreadedConnectionPool(
                config.DB_MINCONN,
                config.DB_MAXCONN,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                host=config.DB_HOST,
                port=config.DB_PORT
            )
            _logger.info("[DB] Successfully init connection pool with info: host=%s, db=%s, port=%s"
                         % (config.DB_HOST, config.DB_NAME, config.DB_PORT))
        except Exception as e:
            _logger.error("[DB] Fail connecting to db with info: host=%s, db=%s, port=%s - ERROR: %s" %
                          (config.DB_HOST, config.DB_NAME, config.DB_PORT, str(e)))
            return False