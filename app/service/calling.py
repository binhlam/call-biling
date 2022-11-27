# -*- coding: utf-8 -*-
from app.domain.model import CallBillingModel
from app.repository.calling import CallingRepository
from app.repository.billing import BillingRepository
import math

BLOCK_DURATION = 30


class CallingService:

    @classmethod
    def compute(cls, duration):
        """
        Function compute total block calls.
        :param duration:
        :return: total blocks
        """
        call_duration_in_second = duration / 1000
        return math.ceil(call_duration_in_second / BLOCK_DURATION)

    @classmethod
    def record(cls, data):
        """
        Function convert & save data
        :param data: request data
        :return:
        """
        call_duration = data.get('call_duration', 1)
        current_blocks = cls.compute(call_duration)
        user_name = data.get('user_name', '')

        # fetch current data
        record = BillingRepository.fetch(user_name)
        call_count = record.get('call_count', 0) + 1
        block_count = current_blocks + record.get('block_count', 0)

        # compute update data
        calling = CallBillingModel({
            'user_name': data.get('user_name', ''),
            'call_count': call_count,
            'block_count': block_count,
        })
        return CallingRepository.record(calling)
