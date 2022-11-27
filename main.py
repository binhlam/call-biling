# -*- coding: utf-8 -*-
from database import ConnectionPool
from configuration import ConfigManager


def run():
    # init config, logger
    config = ConfigManager()
    config.init_logger()

    # init connection pool
    connection_pool = ConnectionPool()
    connection_pool.init_pool(config)

    # init app
    from app import flask_app
    return flask_app


if __name__ == "__main__":
    run()
