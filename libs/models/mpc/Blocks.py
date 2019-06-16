import simplejson as json
import datetime
from ..mpc.Elastic import Elastic
import requests
from boto3.dynamodb.conditions import Key, Attr


class Blocks():
    def __init__(self, dynamo, elastic: Elastic):
        self.__dynamo = dynamo
        self.__elastic = elastic

    @property
    def dynamo(self):
        return self.__dynamo

    @property
    def elastic(self):
        return self.__elastic

    def user_product_type_affinity(self, customer_id):
        response = self.dynamo.query(
            KeyConditionExpression="pk = :pk and begins_with(sk,  :sk)",
            ExpressionAttributeValues={":pk": customer_id, ":sk": "AFFINITY#PRODUCT_TYPE"}
        )

        if 'Items' in response:
            if len(response['Items']) == 1:
                return response['Items'][0]

        return None

    def score_functions(self, scoring_attr, affinity):
        functions_list = []
        for ptype, rating in affinity['rating'].items():
            functions_list.append({
                "filter": {
                    "match": {
                        scoring_attr: ptype
                    }
                },
                "weight": rating
            })
        return functions_list

    def customer_profile(self, customer_id):
        return {
            "customer_id": customer_id,
            "gender": "MENS"
        }

    def product_type_decoration(self):

        meta_lookup = self.dynamo.scan(
            FilterExpression=Key('pk').eq('META_DATA') and Key('sk').eq('product_type_decorate'))

        if 'Items' in meta_lookup:
            return meta_lookup['Items'][0]

        return None

    def parse_gender_product_block(self, content, gender):
        meta_decorate = self.product_type_decoration()
        gender_types_found = []

        for ptype in content['aggregations']['product_types']['buckets']:
            ptypekey = ptype['key']
            ptype_image = None

            if ptypekey in meta_decorate and gender in meta_decorate[ptypekey]['image']:
                ptype_image = meta_decorate[ptypekey]['image'][gender]
                ptype_label = meta_decorate[ptypekey]['label']
            if ptype_image:
                gender_types_found.append(
                    {
                        "label": ptype_label,
                        "image": ptype_image,
                        "type": ptypekey,
                        "url": "catalog/list/{}-{}".format(gender, ptypekey).lower()
                    }
                )

        return gender_types_found

    def parse_products(self, content):
        if 'hits' in content:
            return content['hits']

        return None

    def product_type_by_customer(self, customer_id, result_size=0):
        product_type_affinity = self.user_product_type_affinity(customer_id=customer_id)
        product_type_scoring_functions = self.score_functions("product_type", product_type_affinity)

        customer_pref = self.customer_profile(customer_id)
        category_by_gender_query = {
            "query": {
                "function_score": {
                    "query": {
                        "term": {
                            "gender": {"value": customer_pref['gender']}
                        },
                    },
                    "functions": product_type_scoring_functions
                },
            },
            "aggs": {
                "product_types": {
                    "terms": {
                        "field": "product_type",
                        "order": {
                            "max_score": "desc"
                        }
                    },
                    "aggs": {
                        "max_score": {
                            "max": {
                                "script": "_score"
                            }
                        }
                    }
                }

            },
            "size": result_size
        }

        res = self.elastic.post_search(category_by_gender_query)
        parsed_prod_blocks = self.parse_gender_product_block(res.json(), customer_pref['gender'])
        parsed_products = self.parse_products(res.json())

        return {
            "products": parsed_products,
            "type_blocks": parsed_prod_blocks
        }
