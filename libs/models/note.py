import os
from ..core.dynamo_db import BaseModel


if os.environ['NOTE_TABLE_NAME'] is None:
    raise NotImplementedError('Missing NOTE_TABLE_NAME env var')


class Note(BaseModel):
    table_name = os.environ['NOTE_TABLE_NAME']
