import uuid
import simplejson as json
from . import DecimalEncoder
import boto3
from datetime import datetime
import os


class Base:
    def __init__(self, dydb=None):
        if not dydb:
            self.__db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
        else:
            self.__db = dydb

        if 'MPC_TABLE_NAME' in os.environ:
            self.__tbl = self.__db.Table(os.environ['MPC_TABLE_NAME'])
        else:
            self.__tbl = self.__db.Table('mpcmain')

    def get_table(self):
        return self.__tbl

    @staticmethod
    def dump_json(data):
        return json.dumps(data)

    @staticmethod
    def new_guid():
        return uuid.uuid4().__str__()

    @staticmethod
    def timestamp():
        return datetime.utcnow().__str__()
