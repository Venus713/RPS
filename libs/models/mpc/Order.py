from . import base
from . import Factory
from . import Quote
import uuid

"""
order status:
- PENDING
- PROCESSING
- CANCELED 
- COMPLETE
"""


class Order(base.Base):

    def __init__(self, dydb=None, cognito_id=None):
        guid = self.new_guid()
        self.__db = dydb
        self.__sk = "ORDER#PENDING#{}".format(guid)
        self.__customer_id = cognito_id
        self.__pk = self.__customer_id

        self.__state = 'ORDER'
        self.__status = 'NEW'
        self.__order_id = None
        self.__currency = None
        self.__summary = {}
        self.__items = {}
        self.__shipment = None
        self.__shipping = {}
        self.__billing = None
        self.__address = {}
        self.__coupons = {}
        self.__credit = {}
        self.__payment = {}
        self.__order_number = None

        super(Order, self).__init__(dydb)

    def init_from_quote(self, quote: Quote.Quote):
        self.__state = 'ORDER'
        self.__status = 'NEW'
        self.__currency = quote.currency
        self.__summary = quote.summary.copy()

        del(self.__summary['sk'])
        del(self.__summary['status'])
        self.__summary.update({'pk': quote.new_guid()})
        self.__summary.update({'quote_id': quote.quote_id})

        self.__items = quote.items
        # self.__shipment = quote.shipment
        self.__shipping = quote.shipping
        self.__billing = quote.billing
        self.__address = quote.address
        self.__coupons = quote.coupons
        self.__credit = quote.credit
        self.__order_number = quote.order_number


        return self

    def get_data(self):

        if self.__billing:
            return {
                "customer_id": self.__customer_id,
                "state": self.__state,
                "status": self.__status,
                "currency": self.__currency,
                "summary": self.__summary,
                "items": self.__items,
                "shipment": self.__shipment,
                "shipping": self.__shipping,
                "billing": self.__billing.get_data(),
                "address": self.__address,
                "coupons": self.__coupons,
                "credit": self.__credit,
                "payment": self.__payment,
                "order_number": self.__order_number,
                "sk": self.__sk,
                "pk": self.__pk
            }
        else:
            return {
                "customer_id": self.__customer_id,
                "state": self.__state,
                "status": self.__status,
                "currency": self.__currency,
                "summary": self.__summary,
                "items": self.__items,
                "shipment": self.__shipment,
                "shipping": self.__shipping,
                "address": self.__address,
                "coupons": self.__coupons,
                "credit": self.__credit,
                "payment": self.__payment,
                "order_number": self.__order_number,
                "sk": self.__sk,
                "pk": self.__pk
            }
