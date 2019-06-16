from . import base
import json
import uuid
import datetime


class Config(base.Base):

    def __init__(self, currency='ZAR', dydb=None):
        self.__config = None
        super(Config, self).__init__(dydb)

        last_config = 'CONFIG#2019-06-1'

        response = self.get_table().query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": last_config}
        )

        if 'Items' in response and response['Items'].__len__() == 1:
            self.__config = response['Items'][0]['config']

    @property
    def currencies(self):
        return self.__config['currencies']

    @property
    def base_currency(self):
        return self.__config['base_currency']

    @property
    def payment_methods(self):
        return self.__config['payment_methods']

    @property
    def shipping_methods(self):
        return self.__config['shipping_methods']

