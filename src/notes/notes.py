import json
import uuid
from datetime import datetime
from libs.models.note import Note
from libs.core.response import return_success, return_failure


def index(event, context):
    userId = event['requestContext']['identity']['cognitoIdentityId']
    result = Note.list(userId)

    return return_success(result['Items'])


def create(event, context):
    data = json.loads(event['body'])
    data['userId'] = event['requestContext']['identity']['cognitoIdentityId']
    data['noteId'] = str(uuid.uuid1())
    data['created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = Note.create(data)
        return return_success(data)
    except Exception as e:
        return return_failure(str(e))


def get(event, context):
    key = {
        'userId': event['requestContext']['identity']['cognitoIdentityId'],
        'noteId': event['pathParameters']['id']
    }

    try:
        response = Note.get(key)
        return return_success(response)
    except Exception as e:
        return return_failure(str(e))


def update(event, context):
    key = {
        'userId': event['requestContext']['identity']['cognitoIdentityId'],
        'noteId': event['pathParameters']['id']
    }

    data = json.loads(event['body'])

    try:
        response = Note.update(
            key,
            "SET content = :content, attachment = :attachment",
            {
                ":attachment": data.get('attachment'),
                ":content": data.get('content')
            },
            ReturnValues="ALL_NEW")
        return return_success({'status': True})
    except Exception as e:
        return return_failure(str(e))


def delete(event, context):
    key = {
        'userId': event['requestContext']['identity']['cognitoIdentityId'],
        'noteId': event['pathParameters']['id']
    }

    try:
        response = Note.delete(key)
        return return_success({'status': True})
    except Exception as e:
        return return_failure(str(e))
