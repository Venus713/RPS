from libs.models.note import Note
from libs.core.response import return_success, return_failure


def index(event, context):
    result = Note.list()

    return return_success(result['Items'])
