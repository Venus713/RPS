from . import base
import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
import uuid
from datetime import datetime


class Shipment(base.Base):
    def __init__(self, dydb=None, quote=None):
        self.__quote = quote # __quote : mpc.Quote
        super(Shipment, self).__init__(dydb)

    @property
    def quote(self):
        return self.__quote

    def calculate(self):
        return {'price': 60, 'vat' : 0, 'subtotal': 60}