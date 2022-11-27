# -*- coding: utf-8 -*-
from app.domain.model import CallBillingModel
from app.repository.billing import BillingRepository


class BillingService:

    @classmethod
    def compute(cls, user_name):
        """
        Function fetch calling bill by user_name
        :param user_name:
        :return: data
        """
        record = BillingRepository.fetch(user_name)
        if record is None:
            return record

        data = CallBillingModel(record)
        return data
