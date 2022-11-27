# -*- coding: utf-8 -*-
from app.domain.model import CallBillingModel
from app.repository.calling import CallingRepository
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
        call_duration = data.get('call_duration', 0)
        total_blocks = cls.compute(call_duration)
        calling = CallBillingModel({
            'user_name': data.get('user_name', ''),
            'block_count': total_blocks,
        })
        return CallingRepository.record(calling)
