from libs.models.mpc.Blocks import Blocks
from libs.core.response import return_success, return_failure
from libs.models.mpc.Blocks import Blocks
from libs.models.mpc.Elastic import Elastic
import simplejson as json
import boto3
import os
from requests_aws4auth import AWS4Auth

region = os.environ['APP_REGION']
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)

es_host = os.environ['ES_HOST_URL']
host = es_host
elastic = Elastic(host=host, awsauth=awsauth)

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(os.environ['MPC_TABLE_NAME'])


def customer_affinity(event, context):
    customer_id = event['requestContext']['identity']['cognitoIdentityId']

    if customer_id:
        custom_blocks = Blocks(dynamo=table, elastic=elastic)
        affinity = custom_blocks.user_product_type_affinity(customer_id)
        return return_success(affinity)

    return "Nothing"


def shop_by_category(event, context):
    customer_id = event['requestContext']['identity']['cognitoIdentityId']

    if customer_id:
        custom_blocks = Blocks(dynamo=table, elastic=elastic, )
        results = custom_blocks.product_type_by_customer(customer_id=customer_id)
        return return_success(results)

    return "Nothing"
