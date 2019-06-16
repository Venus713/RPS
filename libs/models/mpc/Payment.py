import decimal
from . import base

from . import Factory
from . Config import Config
import uuid


class Payment(base.Base):

    def __init__(self,
                 dydb=None,
                 cognito_id=None,
                 amount=0,
                 shipping_amount=0,
                 order_number=None,
                 rate=1
                 ):
        self.__db = dydb

        self.__sk = "PAYMENT#{}".format(self.new_guid())
        self.__pk = None
        self.__method = None
        self.__action = None
        self.__amount = amount
        self.__order_number = order_number
        self.__shipping_amount = shipping_amount
        self.__account_status = None
        self.__additional_data = None
        self.__last_trans_id = None

        self.__base_amounts = {
            "pending": {
                "amount_authorized": None,
                "amount_ordered": None,
                "shipping_amount": None,
            },
            "captured": {
                "amount_paid": None,
                "amount_paid_online": None,
                "shipping_captured": None,
            },
            "canceled": {
                "amount_canceled": None,
            },
            "refunded": {
                "amount_refunded": None,
                "amount_refunded_online": None,
                "shipping_refunded": None,
            }
        }

        self.__real_amounts = {
            "pending": {
                "amount_authorized": None,
                "amount_ordered": None,
                "shipping_amount": None,
            },
            "captured": {
                "amount_paid": None,
                "amount_paid_online": None,
                "shipping_captured": None,
            },
            "canceled": {
                "amount_canceled": None,
            },
            "refunded": {
                "amount_refunded": None,
                "amount_refunded_online": None,
                "shipping_refunded": None,
            }
        }

        self.__base_amounts['pending']['amount_ordered'] = decimal.Decimal(self.__amount)
        self.__base_amounts['pending']['shipping_amount'] = decimal.Decimal(self.__shipping_amount)

        self.__real_amounts['pending']['amount_ordered'] =  self.__base_amounts['pending']['amount_ordered'] * rate
        self.__real_amounts['pending']['shipping_amount'] = self.__base_amounts['pending']['shipping_amount'] * rate



        super(Payment, self).__init__(dydb)

    def get_data(self):
        return {
            "method": self.__method,
            "sk": self.__sk,
            "pk": self.__pk,
            "account_status": self.__account_status,
            "additional_data": self.__additional_data,
            "last_trans_id": self.__last_trans_id,
            "base_amounts": self.__base_amounts,
            "real_amounts": self.__real_amounts
        }

    @property
    def pk(self):
        return self.__pk

    @pk.setter
    def pk(self, pk):
        self.__pk = pk

    @property
    def outstanding(self):
        return self.__real_amounts['pending']['amount_ordered']

    @property
    def order_number(self):
        return self.__order_number

    @order_number.setter
    def order_number(self, ordernum):
        self.__order_number = ordernum

    @property
    def method(self):
        if self.__method:
            return self.__method.name

        return "N/A"

    @method.setter
    def method(self, method):
        self.__method = method

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        self.__action = action

    def set_base_amount(self, fld, amount):
        self.__base_amounts[fld] = amount

    def set_real_amount(self, fld, amount):
        self.__real_amounts[fld] = amount


    def capture(self):
        print("Outstanding: ",self.outstanding)
        return True