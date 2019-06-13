from libs.models.category import Category
from libs.core.response import return_success, return_failure


def list(event, context):
    result = Category.list()

    return return_success(result['Items'])
