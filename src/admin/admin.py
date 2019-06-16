"""
reset elastic index
"""
import os
import requests
import boto3
import decimal
from requests_aws4auth import AWS4Auth

#'eu-west-1'
region = os.environ['APP_REGION']
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)

#'search-mpc-sls-es-development-cl2-4ub2ooanjdpbxsib4fomhkjzha.eu-west-1.es.amazonaws.com'
host = os.environ['ES_HOST_URL']

#'mpc-products-v8'
index_name = os.environ['ES_INDEX_NAME']

doc_type = 'products'
mapping_url = 'https://' + host + '/' + index_name

# 'dev-mpcmain'
dynamo_table_name = os.environ['MPC_TABLE_NAME']
dynamodbclient = boto3.resource('dynamodb')

products_mapping = {
    "mappings": {
        "products": {
            "properties": {
                "discount": {
                    "type": "long"
                },
                "event_id": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "gender": {
                    "type": "keyword"
                },
                "images": {
                    "properties": {
                        "delete": {
                            "type": "long"
                        },
                        "position": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "s3_filepath": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                },
                "manufacturer": {
                    "type": "keyword"
                },
                "portal_config_id": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "prices": {
                    "properties": {
                        "ZAR": {
                            "properties": {
                                "cost_price_excl_vat": {
                                    "type": "float"
                                },
                                "cost_price_incl_vat": {
                                    "type": "float"
                                },
                                "currency": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                },
                                "rate": {
                                    "type": "float"
                                },
                                "rrp": {
                                    "type": "float"
                                },
                                "rrp_rounded": {
                                    "type": "long"
                                },
                                "rs_price_with_mark_up": {
                                    "type": "float"
                                },
                                "selling_price": {
                                    "type": "float"
                                },
                                "symbol": {
                                    "type": "text",
                                    "fields": {
                                        "keyword": {
                                            "type": "keyword",
                                            "ignore_above": 256
                                        }
                                    }
                                },
                                "wsp": {
                                    "type": "float"
                                }
                            }
                        }
                    }
                },
                "product_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "rs_colour": {
                    "type": "keyword"
                },
                "rs_event_code": {
                    "type": "keyword",
                },
                "rs_product_sub_type": {
                    "type": "keyword",
                },
                "product_type": {
                    "type": "keyword",
                },
                "season": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "size_chart": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "sizes": {
                    "properties": {
                        "portal_config_id": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "portal_simple_id": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "qty": {
                            "type": "long"
                        },
                        "rs_simple_sku": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "size_tag": {
                            "type": "keyword",
                        },
                        "size": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "status": {
                            "type": "long"
                        }
                    }
                },
                "sku": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "status": {
                    "type": "long"
                },
                "supplier": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                }
            }
        }
    }
}


def reset(event, lambda_context):
    headers = {"Content-Type": "application/json"}
    res = requests.put(mapping_url, json=products_mapping, headers=headers, auth=awsauth)
    return res.text


def set_config(event, lambda_context):
    table = dynamodbclient.Table(dynamo_table_name)
    table.put_item(Item={
        "pk": "CONFIG#2019-06-1",
        "sk": "SITE",
        "config": {
            'payment_methods': {
                'banktransfer': {
                    "label": "EFT Payment",
                    "position": 1,
                    "active": 1,
                    "allowed_countries": ["ZA"]
                },
                'peach_payment': {
                    "label": "CC Payment",
                    "position": 2,
                    "active": 0,
                    "allowed_countries": ["ZA"]
                },
            },
            'shipping_methods': {
                'standard': {
                    "label": "Standard Shipping",
                    "position": 1,
                    "active": 1,
                    "allowed_countries": ["ZA"]
                },
                'express': {
                    "label": "Express Shipping",
                    "position": 2,
                    "active": 0,
                    "allowed_countries": ["ZA"]
                },
            },
            "base_currency": "ZAR",
            "currencies": {
                "ZAR": {
                    "rate": decimal.Decimal(1.0),
                    "last_update": "2019-01-01 00:00:00"
                },
            }
        }
    })

    table.put_item(Item={
        "pk": "a59f680e-e727-40f8-86bd-f6f3e844fd21",
        "sk": "AFFINITY#PRODUCT_TYPE",
        "gender": "MENS",
        "rating": {
            "WATCHES": "0",
            "JACKETS": "0",
            "TOPS": "0",
            "SHOES": "0",
            "WALLETS": "0",
            "ACCESSORIES": "0",
            "BOTTOMS": "0",
            "BELTS": "0",
            "BAGS": "0",
            "COSMETICS": "0"
        }
    })

    table.put_item(Item={
        "pk": "META_DATA",
        "sk": "product_type_decorate",
        "SHOES": {
            "label": "Shoes",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "COSMETICS": {
            "label": "Cosmetics",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "SUNGLASSES": {
            "label": "Sunglasses",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "BAGS": {
            "label": "Bags",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "WATCHES": {
            "label": "Watches",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "JACKETS": {
            "label": "Jackets",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "TOPS": {
            "label": "Tops",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "BOTTOMS": {
            "label": "Bottoms",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "WALLETS": {
            "label": "Wallets",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        },
        "DRESSES": {
            "label": "Dresses",
            "image": {
                "LADIES": "http://lorempixel.com/100/100/people",
                "MENS": "http://lorempixel.com/100/100/people",
                "UNISEX": "http://lorempixel.com/100/100/people",
                "KIDS": "http://lorempixel.com/100/100/people",
                "INFANTS": "http://lorempixel.com/100/100/people"
            }
        }
    })
