import os
import json
import boto3
dynamodb = boto3.resource('dynamodb')


def list(event, context):
    table = dynamodb.Table(os.environ['CATEGORY_TABLE_NAME'])
    result = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response
