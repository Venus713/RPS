"""
reset elastic index
"""
import requests
import boto3
import simplejson as json
from requests_aws4auth import AWS4Auth
from decimal import Decimal, getcontext, setcontext, Context as DecimalContext, ROUND_05UP, ROUND_UP, ROUND_HALF_EVEN, \
    ROUND_DOWN

region = 'eu-west-1'
service = 'es'
dynamo_table_name ='dev-mpcmain'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'search-mpc-sls-es-development-cl2-4ub2ooanjdpbxsib4fomhkjzha.eu-west-1.es.amazonaws.com'
index_name = 'mpc-products-v8'
doc_type = 'products'
index_url = 'https://' + host + '/mpc-products-v8/' + doc_type
dynamodbclient = boto3.resource('dynamodb')

headers = {"Content-Type": "application/json"}

must_be_decimal = ["rrp_rounded", "rrp", "wsp", "cost_price_excl_vat", "cost_price_incl_vat", "rs_price_with_mark_up",
                   "selling_price", "rate"]
can_remove = ["supplier_product_name", "rs_sku", "product_size_attribute", "supplier_sku", "product_description",
              "rs_selling_price"]

currency_fields = ["rrp_rounded", "rrp", "wsp", "cost_price_excl_vat", "cost_price_incl_vat", "rs_price_with_mark_up",
                   "selling_price"]


def strip_blanks(data):
    remove = []
    for k in data:
        if data[k] == '' or data[k] == None:
            remove.append(k)

    for k in remove:
        del (data[k])


def clean_values(data):
    for k in must_be_decimal:
        if k in data:
            if data[k]:
                strval = str(data[k])
                strplit = strval.split('.')
                if len(strplit) > 1:
                    strplit[1] = strplit[1][0:2]
                strval = '.'.join(str(s) for s in strplit)
                data[k] = strval
                data[k] = float(data[k])

    return data


def convert_decimal(data):
    context = DecimalContext(prec=10, rounding=ROUND_DOWN)
    for prices in data['prices']:
        for fld in must_be_decimal:
            v = data['prices'][prices][fld]
            if v:
                v = round(v, 2)
                v = context.create_decimal_from_float(v)
            else:
                v = context.create_decimal_from_float(0)

            data['prices'][prices][fld] = v

    return data


def update_products_db(pdata):
    converteddata = convert_decimal(pdata)
    converteddata.update({'pk': converteddata['sku']})
    converteddata.update({'sk': "PRODUCT"})
    strip_blanks(converteddata)

    product_table = dynamodbclient.Table(dynamo_table_name)
    product_table.put_item(Item=pdata)


def add_to_es(datadict):
    requests.put(index_url + '/' + datadict['sku'], json=datadict, headers=headers, auth=awsauth)


def prepare_product(datadict):
    datadict.update({'selling_price': datadict['rs_selling_price']})
    datadict = clean_values(datadict)
    datadict = dict(datadict)
    datadict.update({'sku': datadict['rs_sku']})
    datadict.update({'product_type': datadict['product_size_attribute']})
    for rem in can_remove:
        del (datadict[rem])

    base = dict()
    for cf in currency_fields:
        base.update({cf: datadict[cf]})

    base.update({'currency': 'ZAR'})
    base.update({'rate': 1.0})
    base.update({'symbol': 'R'})
    currencies = {'ZAR': base}
    datadict.update({'prices': currencies})

    for rem in must_be_decimal:
        if rem in datadict:
            del (datadict[rem])

    if 'sizes' in datadict:
        for size in datadict['sizes']:
            size.update({"size_tag": "{}|{}|{}|{}".format(
                datadict['gender'],
                datadict['product_type'],
                datadict['manufacturer'],
                size['size'])
            })

    add_to_es(datadict)

    sizes = {}
    if 'sizes' in datadict:
        for size in datadict['sizes']:
            sizes.update({size['rs_simple_sku']: size.copy()})

    datadict.update({'sizes': sizes})
    update_products_db(datadict)


def import_product(event, lambda_context):
    data = event['body']
    data = json.loads(data)
    prepare_product(data)

    # if 'Records' in event:
    #     for rec in event['Records']:
    #         product = json.loads(rec['body'])
    #         r = requests.put(index_url+'/'+product['rs_sku'], auth=awsauth, json=product, headers=headers)
    #         body = {
    #             "message": "SENT",
    #         }

    response = {
        "statusCode": 200
    }
    return response
