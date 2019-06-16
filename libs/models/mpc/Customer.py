from . import base
from . import Address
from . import Factory
import uuid


class Customer(base.Base):

    def __init__(self, dydb=None, cognito_id=None):

        self.address_api = Address.Address(dydb=dydb)
        self.__db = dydb
        self.__firstname = None
        self.__lastname = None
        self.__email = None
        self.__gender = None
        self.__newsletters = {}
        self.__default_billing_address = None
        self.__default_shipping_address = None
        self.__sk = "CUSTOMER"

        if not cognito_id:
            self.__customer_id = uuid.uuid4().__str__()
        else:
            self.__customer_id = cognito_id

        self.__pk = self.__customer_id

        super(Customer, self).__init__(dydb)

    def __str__(self):
        return self.dump_json(self.get_data())

    def get_data(self):
        return {
            "firstname": self.__firstname,
            "lastname": self.__lastname,
            "email": self.__email,
            "gender": self.__gender,
            "newsletters": self.__newsletters,
            "default_billing_address": self.__default_billing_address,
            "default_shipping_address": self.__default_shipping_address,
            "sk": self.__sk,
            "pk": self.__pk
        }

    def save(self):
        try:
            response = self.get_table().put_item(Item=self.get_data())
            if 'ResponseMetadata' in response:
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return True
        except:
            return False

    def load(self, pk):
        response = self.get_table().query(
            KeyConditionExpression="pk = :pk and sk = :sk",
            ExpressionAttributeValues={":pk": pk, ":sk": self.__sk}
        )

        if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            items = response['Items']
            if items.__len__() > 0:
                customer_data = response['Items'][0]
                self.pk = customer_data['pk']
                self.sk = customer_data['sk']
                self.firstname = customer_data["firstname"]
                self.lastname = customer_data["lastname"]
                self.email = customer_data["email"]
                self.gender = customer_data["gender"]
                self.default_billing_address = customer_data["default_billing_address"]
                self.default_shipping_address = customer_data["default_shipping_address"]
                self.newsletters = customer_data["newsletters"]
            else:
                self.pk = pk
                self.sk = "CUSTOMER"
                self.firstname = "Guest"
                self.lastname = "User"
                self.email = None
                self.gender = None
                self.default_billing_address = None
                self.default_shipping_address = None
                self.newsletters = {}

            return self

        return False

    @property
    def newsletters(self):
        return self.__newsletters

    @newsletters.setter
    def newsletters(self, newsletters):
        self.__newsletters = newsletters

    @property
    def pk(self):
        return self.__pk

    @pk.setter
    def pk(self, pk):
        self.__pk = pk

    @property
    def firstname(self):
        return self.__firstname

    @firstname.setter
    def firstname(self, firstname):
        self.__firstname = firstname

    @property
    def lastname(self):
        return self.__lastname

    @lastname.setter
    def lastname(self, lastname):
        self.__lastname = lastname

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender):
        self.__gender = gender

    @property
    def default_billing_address(self):
        return self.__default_billing_address

    @default_billing_address.setter
    def default_billing_address(self, default_billing_address):
        self.__default_billing_address = default_billing_address

    @property
    def default_shipping_address(self):
        return self.__default_shipping_address

    @default_shipping_address.setter
    def default_shipping_address(self, default_shipping_address):
        self.__default_shipping_address = default_shipping_address

    def add_newsletter(self, newsletter_name):
        self.__newsletters.update({newsletter_name: True}),

    def remove_newsletter(self, newsletter_name):
        del (self.__newsletters[newsletter_name])
