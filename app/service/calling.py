# -*- coding: utf-8 -*-
from app.domain.model import CallBillingModel
from app.repository.calling import CallingRepository
from .postgres import transaction
import math
import logging
import psycopg2, psycopg2.extras

_logger = logging.getLogger('call-billing')
BLOCK_DURATION_IN_SECOND = 30


class CallingService(object):
    def compute(self, duration):
        """
        Function compute total block calls.
        :param duration:
        :return: total blocks
        """
        call_duration_in_second = duration / 1000
        return math.ceil(call_duration_in_second / BLOCK_DURATION_IN_SECOND)

    def record(self, data):
        """
        Function convert & save data
        :param data: request data
        :return:
        """
        with transaction() as conn:
            cr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            repo = CallingRepository(cr=cr)

            call_duration = data.get('call_duration', 1)
            current_block_count = self.compute(call_duration)
            user_name = data.get('user_name', '')

            # lock current record (pessimistic locking)
            record = repo.lock(user_name)
            _logger.info("[CallingService] lock success with user: %s" % user_name)

            call_count = record.get('call_count', 0) + 1
            block_count = current_block_count + record.get('block_count', 0)

            # update data
            calling = CallBillingModel({
                'user_name': user_name,
                'call_count': call_count,
                'block_count': block_count,
            })
            res = repo.save(calling)
            _logger.info("[CallingService] record success with user: %s" % user_name)

            return res
