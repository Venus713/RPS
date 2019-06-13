import os
from ..core.dynamo_db import BaseModel


if os.environ['CATEGORY_TABLE_NAME'] is None:
    raise NotImplementedError('Missing CATEGORY_TABLE_NAME env var')


class Category(BaseModel):
    table_name = os.environ['CATEGORY_TABLE_NAME']
