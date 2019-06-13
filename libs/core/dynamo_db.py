import boto3
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
    def list(cls, **kwargs):
        if cls.table_name is None:
            raise NotImplementedError('Missing table_name')
        return dynamodb.Table(cls.table_name).scan()
