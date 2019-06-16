from . import base
from ..mpc.Shipment import Shipment
from ..mpc.Product import Product
from ..mpc.Config import Config
import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
import uuid
import datetime
import random
import string


class Quote(base.Base):
    product_api = None  # type: mpc.Product

    def __init__(self, currency='ZAR', dydb=None, qid=None, country_code=None, rate=1.0):
        self.__dydb = dydb
        self.__customer_id = None
        self.__state = 'QUOTE'
        self.__status = 'NEW'
        self.__quote_id = None
        self.__order_id = None
        self.__currency = currency
        self.__currency_rate = rate
        self.__summary = {}
        self.__payment_method = None
        self.__shipping_method = None
        self.__items = {}
        self.__shipment = Shipment(dydb=dydb, quote=self)
        self.__shipping = {}
        self.__billing = {}
        self.__address = {}
        self.__coupons = {}
        self.__credit = {}
        self.__order_number = self.generate_order_number()
        self.__country_code = country_code

        super(Quote, self).__init__(dydb)

        if qid:
            self.__quote_id = qid

        if not self.__quote_id:
            self.__quote_id = uuid.uuid4().__str__()
            self.set_status("NEW")
            self.__created_at = self.timestamp()

        self.product_api = Product(dydb=dydb)

    def __str__(self):
        return self.dump_json({
            "summary": self.__summary,
            "items": self.__items,
            "shippping": self.__shipping
        })

    def generate_order_number(self):
        # code = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
        code = 101
        return datetime.datetime.now().strftime("%y%m%d{}0%f".format(code))

    @property
    def shipping_method(self):
        return self.__shipping_method

    @property
    def payment_method(self):
        return self.__payment_method

    @property
    def shipment(self):
        return self.__shipment

    @property
    def order_number(self):
        return self.__order_number

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, currency):
        self.__currency = currency

    @property
    def currency_rate(self):
        return self.__currency_rate

    @currency_rate.setter
    def currency_rate(self, currency_rate):
        self.__currency_rate = currency_rate

    @property
    def address(self):
        return self.__address

    @property
    def coupons(self):
        return self.__coupons

    @property
    def credit(self):
        return self.__credit

    @property
    def shipping(self):
        return self.__shipping

    @shipping.setter
    def shipping(self, shipping):
        self.__shipping = shipping

    @property
    def billing(self):
        return self.__billing

    @billing.setter
    def billing(self, billing):
        self.__billing = billing

    @property
    def summary(self):
        return self.__summary

    @property
    def items(self):
        return self.__items

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, cid):
        self.__customer_id = cid

    @property
    def quote_id(self):
        return self.__quote_id

    @quote_id.setter
    def quote_id(self, qid):
        self.__quote_id = qid

    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, oid):
        self.__order_id = oid

        # KeyConditionExpression = "pk = :pk and begins_with(sk, :sk)",

    def set_payment_method(self, method):
        """
        Set payment method to be used.
        :param method:
        :return:
        """
        # TODO: validate payment method option
        self.__payment_method = method

    def set_shipment_method(self, method):
        """
        Set shipment method on quote
        :param method: string
        :return:
        """
        self.__shipping_method = method

    def make_item(self, product, qty):
        return {
            "pk": self.get_quote_id(),
            "sk": "QITEM|{}".format(product['sku']),
            "id": uuid.uuid4().__str__(),
            "qty": qty,
            "price": product['price'],
            "sku": product['sku']
        }

    @staticmethod
    def validate_cart_string(cart_string):
        try:
            sku, size, qty = cart_string.split('#')
        except ValueError:
            raise Exception("Error reading add-to-cart request")

        if sku is None or size is None or qty is None:
            raise Exception("Invalid add to cart request")

        return {'sku': sku, 'size': size, 'qty': int(qty)}

    def validate_items(self):
        if self.product_api:
            for item_id, item in self.__items.items():
                sk = item['sk'].split('#')
                product = self.product_api.get_size(sk[1], sk[2])
                if int(product['qty']) < int(item['qty']):
                    item.update({"error": "Qty Unavailable"})

                # item.update({"images": product['images']})
        self.refresh_summary()

    def add_cart_item(self, sku, size, qty, product):
        itemindex = "QI#{}#{}".format(sku, size)

        if itemindex in self.__items:
            # exists
            qty = int(qty) + int(self.__items[itemindex]['qty'])

        if int(qty) <= int(product['sizes'][size]['qty']) and int(product['sizes'][size]['status']) == 0:
            size_selected = product['sizes'][size].copy()
        else:
            raise Exception("Requested quantity not available : {}".format(size))

        size_selected.update({
            'sku': size_selected['rs_simple_sku'],
            'qty': qty,
            'name': product['product_name'],
            'images': product['images'],
            'sk': itemindex,
            'pk': self.quote_id
        })

        del (size_selected['status'])
        del (size_selected['rs_simple_sku'])

        size_selected.update({"prices": product['prices']})
        self.__items.update({itemindex: size_selected})
        return size_selected

    def update_cart_item(self, sku, size, qty, product):
        itemindex = "QI#{}#{}".format(sku, size)

        if int(qty) <= int(product['sizes'][size]['qty']) and int(product['sizes'][size]['status']) == 0:
            size_selected = product['sizes'][size].copy()
        else:
            raise Exception("Requested quantity not available")

        size_selected.update({
            'sku': size_selected['rs_simple_sku'],
            'qty': qty,
            'name': product['product_name'],
            'images': product['images'],
            'sk': itemindex,
            'pk': self.quote_id
        })

        del (size_selected['status'])
        del (size_selected['rs_simple_sku'])

        size_selected.update({"prices": product['prices']})
        self.__items.update({itemindex: size_selected})
        return size_selected

    def update_cart_item(self, sku, size, qty, product):
        print("\n***************Update ITEM***********\n")
        itemindex = "QI#{}#{}".format(sku, size)

        if int(qty) <= int(product['sizes'][size]['qty']) and int(product['sizes'][size]['status']) == 0:
            size_selected = product['sizes'][size].copy()
        else:
            raise Exception("Requested quantity not available")

        size_selected.update({
            'sku': size_selected['rs_simple_sku'],
            'qty': qty,
            'name': product['product_name'],
            'images': product['images'],
            'sk': itemindex,
            'pk': self.quote_id
        })

        del (size_selected['status'])
        del (size_selected['rs_simple_sku'])

        size_selected.update({"prices": product['prices']})
        self.__items.update({itemindex: size_selected})
        return size_selected

    def get_quote(self):
        if not self.quote:
            date = datetime.now().isoformat()
            self.quote = {
                "pk": self.get_quote_id(),
                "sk": "QUOTE|{}".format(date),
                "customer_id": self.customer,
                "total": 0
            }
        return self.quote

    def quote_item(self, sku, qty):
        item = self.get_size(sku)
        return self.extract_item(item, qty)

    def get_quote_id(self):
        if not self.quote_id:
            self.quote_id = uuid.uuid4().__str__()

        return self.quote_id

    # def add_to_cart(self, sku, size, qty, single):
    #     item_id = uuid.uuid4().__str__()
    #     qi = {
    #         "pk": self.get_quote_id(),
    #         "sk": "QITEM|{}".format(item_id),
    #         "id": item_id,
    #         "qty": qty,
    #         "price": single['price'],
    #         "sku": single['sku'],
    #         "size": size
    #     }
    #
    #     return qi

    def write(self, data):
        return self.get_table().put_item(Item=data)

    def remove_item(self, sku, size):
        print("\n***************Update ITEM***********\n")
        itemindex = "QI#{}#{}".format(sku, size)
        if itemindex in self.__items:
            todel = self.__items[itemindex]

            deleteme = {
                "pk": todel['pk'],
                "sk": todel['sk']
            }

            print(deleteme)
            # with self.get_table().batch_writer() as batch:
            print("\n***************Update ITEM from DB***********\n")
            res = self.get_table().delete_item(Key=deleteme)
            print(res)
            if 'ResponseMetadata' in res and res['ResponseMetadata']['HTTPStatusCode'] == 200:
                del (self.__items[itemindex])
                return True

        return False

    def set_qty(self, item_id, qty):

        response = self.tbl.update_item(
            Key={
                "pk": self.get_quote_id(),
                "sk": "QITEM|{}".format(item_id)
            },
            ExpressionAttributeNames={'#QTY': 'qty'},
            ExpressionAttributeValues={":QTY": qty},
            UpdateExpression="SET #QTY = :QTY"
        )

        if 'ResponseMetadata' in response:
            return response['ResponseMetadata']['HTTPStatusCode'] == 200

        print(response)
        # get item
        # increase qty
        # save item

    def refresh_summary(self):
        self.__shipping = self.shipment.calculate()

        print("ONUMBER: ", self.__order_number)

        self.__summary = {
            'pk': self.__quote_id,
            'sk': self.__state,
            'order_number': self.__order_number,
            'payment_method': self.__payment_method,
            'shipping_method': self.__shipping_method,
            'item_qty': 0,
            'subtotal': {'ZAR': 0},
            'status': self.__status,
            'country_code': self.__country_code,
            'created_at': self.__created_at
        }

        for item_id, item in self.__items.items():
            self.__summary['item_qty'] += int(item['qty'])
            self.__summary['subtotal']['ZAR'] += float(item['prices']['ZAR']['selling_price']) * int(item['qty'])

        self.__summary['subtotal']['ZAR'] += self.__shipping['subtotal']
        self.__summary['subtotal']['ZAR'] = self.format_decimal(self.__summary['subtotal']['ZAR'])

    @property
    def total(self):
        return self.summary['subtotal'][self.currency]

    @property
    def shipping_amount(self):
        return self.__shipping['subtotal']

    def save_quote(self):
        """
        If no order number [new order] then generate
        refresh quote summary - calc totals
        update items
        update summary
        :return:
        """
        if not self.__order_number:
            self.__order_number = self.generate_order_number()

        self.refresh_summary()
        for item_id, item in self.__items.items():
            self.write(item)

        self.write(self.__summary)
        return self.quote_id

    def load_quote(self):
        if self.__quote_id:
            response = self.get_table().query(
                KeyConditionExpression="pk = :pk",
                ExpressionAttributeValues={":pk": self.__quote_id}
            )
            if 'Items' in response:
                for entry in response['Items']:
                    if 'sk' in entry:
                        if entry['sk'][0:3] == 'QI#':
                            self.__items.update({entry['sk']: entry})
                        if entry['sk'] == 'QUOTE':
                            self.__summary.update(entry)
                            self.__order_number = self.summary['order_number']
                            self.__shipping_method = self.summary['shipping_method']
                            self.__payment_method = self.summary['payment_method']
                            self.__country_code = self.summary['country_code']
                            self.__status = self.summary['status']
                            self.__created_at = self.summary['created_at']

            # loading currency rate
            config = Config(dydb=self.__dydb)
            currencies = config.currencies
            self.currency_rate = currencies[self.currency]['rate']
            ############################################################

            self.refresh_summary()
        else:
            raise Exception("Unable to load quote, invalid quote ID")

    def format_decimal(self, amount):
        res = "{:.2f}".format(amount)
        return res

    def set_status(self, status):
        if self.__quote_id:

            response = self.get_table().update_item(
                Key={
                    "pk": self.__quote_id,
                    "sk": "QUOTE"
                },
                ExpressionAttributeNames={'#STATUS': 'status'},
                ExpressionAttributeValues={":STATUS": status},
                UpdateExpression="SET #STATUS = :STATUS"
            )
            if 'ResponseMetadata' in response:
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    status_log = {
                        "pk": self.__quote_id,
                        "sk": "STATUS#QUOTE#{}".format(status),
                        "status": status,
                        "updated_at": self.timestamp()
                    }
                    self.get_table().put_item(Item=status_log)

                    return True
        return False

    def set_status_processing(self):
        return self.set_status("PROCESSING")

    def set_status_pending_payment(self):
        return self.set_status("PENDING_PAYMENT")
