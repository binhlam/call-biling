# -*- coding: utf-8 -*-
import configparser
import os
import logging
from app.config.setting import __ENV_VARIABLES__

config = {}
# _logger = None

base_path = os.path.dirname(__file__)
fileHandler_path = os.path.abspath(os.path.join(base_path, "{}".format('log/call-billing.log')))
os.makedirs(os.path.dirname(fileHandler_path), exist_ok=True)

__CONFIG_FILE__ = []
__DEFAULT_SECTION__ = 'environment'


class ConfigManager(object):
    def __init__(self):
        self.config = configparser.RawConfigParser(allow_no_value=True)
        for key, value in __ENV_VARIABLES__.items():
            setattr(self, key, value)
            if not self.config.has_section(__DEFAULT_SECTION__):
                self.config.add_section(__DEFAULT_SECTION__)
            self.config.set(
                section=__DEFAULT_SECTION__,
                option=key,
                value=value
            )

    def get(self, sect, key, default=None):
        try:
            res = self.config.get(sect, key)
        except:
            res = default
        return res

    def __getitem__(self, key):
        return self.config.get(__DEFAULT_SECTION__, key)

    def init_logger(self, logger_name='call-billing'):
        log_format = "%(asctime)s - %(levelname)s - %(name)s - %(filename)s::%(lineno)d - %(message)s"
        formatter = logging.Formatter(log_format)

        fileHandler = logging.FileHandler(fileHandler_path)
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(formatter)

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(fileHandler)
        return logger
