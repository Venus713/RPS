import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')


class BaseModel(object):
    table_name = None
    table = None

    def __init__(self, *args, **kwargs):
        if kwargs.get('table_name') is not None:
            self.table_name = table_name
        if self.table_name is None:
            raise NotImplementedError('Mising table_name')
        else:
            self.table = dynamodb[self.table_name]

    @classmethod
    def get_table(cls):
        if cls.table_name is None:
            raise NotImplementedError('Missing table_name')
        return dynamodb.Table(cls.table_name)

    @classmethod
    def list(cls, userId, **kwargs):
        KeyConditionExpression = kwargs.get('KeyConditionExpression', None)
        if KeyConditionExpression is None:
            KeyConditionExpression = Key('userId').eq(userId)
        else:
            KeyConditionExpression = \
                KeyConditionExpression & Key('userId').eq(userId)
        table = cls.get_table()
        return table.query(
            KeyConditionExpression=KeyConditionExpression, **kwargs)

    @classmethod
    def create(cls, item):
        table = cls.get_table()
        return table.put_item(Item=item)

    @classmethod
    def get(cls, param):
        table = cls.get_table()
        return table.get_item(Key=param)['Item']

    @classmethod
    def update(
            cls, Key, UpdateExpression, ExpressionAttributeValues={},
            ReturnValues='UPDATED_NEW', **kwargs):
        table = cls.get_table()

        return table.update_item(
            Key=Key, UpdateExpression=UpdateExpression,
            ExpressionAttributeValues=ExpressionAttributeValues,
            ReturnValues=ReturnValues, **kwargs)

    @classmethod
    def delete(cls, Key, **kwargs):
        table = cls.get_table()
        return table.delete_item(Key=Key, **kwargs)
