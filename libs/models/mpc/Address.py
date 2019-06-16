from . import base
import uuid


class Address(base.Base):
    def __init__(self, dydb=None):
        self.__customer_pk = None
        self.__type = None
        self.__address_name = None
        self.__company_name = None
        self.__firstname = None
        self.__lastname = None
        self.__email = None
        self.__street1 = None
        self.__street2 = None
        self.__suburb = None
        self.__postcode = None
        self.__city = None
        self.__province = None
        self.__country = None
        self.__telephone = None
        self.__created_at = None
        self.__updated_at = None
        self.__sk = None
        self.__pk = None

        super(Address, self).__init__(dydb)

    def get_data(self):
        return {
            "type": self.__type,
            "address_name": self.__address_name,
            "firstname": self.__firstname,
            "lastname": self.__lastname,
            "email": self.__email,
            "street1": self.__street1,
            "street2": self.__street2,
            "suburb": self.__suburb,
            "postcode": self.__postcode,
            "city": self.__city,
            "province": self.__province,
            "country": self.__country,
            "telephone": self.__telephone,
            "company_name": self.__company_name,
            "sk": self.__sk,
            "pk": self.__pk,
            "customer_pk": self.__customer_pk,
        }

    def save(self):
        try:
            response = self.get_table().put_item(Item=self.get_data())
            if 'ResponseMetadata' in response:
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return True
        except:
            return False

    def __str__(self):
        return self.dump_json(self.get_data())

    @property
    def customer_pk(self):
        return self.__customer_pk

    @customer_pk.setter
    def customer_pk(self, customer_pk):
        self.__customer_pk = customer_pk

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def address_name(self):
        return self.__address_name

    @address_name.setter
    def address_name(self, address_name):
        self.__address_name = address_name

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
    def street1(self):
        return self.__street1

    @street1.setter
    def street1(self, street1):
        self.__street1 = street1

    @property
    def street2(self):
        return self.__street2

    @street2.setter
    def street2(self, street2):
        self.__street2 = street2

    @property
    def suburb(self):
        return self.__suburb

    @suburb.setter
    def suburb(self, suburb):
        self.__suburb = suburb

    @property
    def postcode(self):
        return self.__postcode

    @postcode.setter
    def postcode(self, postcode):
        self.__postcode = postcode

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    @property
    def province(self):
        return self.__province

    @province.setter
    def province(self, province):
        self.__province = province

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, country):
        self.__country = country

    @property
    def telephone(self):
        return self.__telephone

    @telephone.setter
    def telephone(self, telephone):
        self.__telephone = telephone

    @property
    def created_at(self):
        return self.created_at

    @property
    def updated_at(self):
        return self.__updated_at

    @property
    def sk(self):
        return self.__sk

    @sk.setter
    def sk(self, sk):
        self.__sk = sk

    @property
    def pk(self):
        return self.__pk

    @pk.setter
    def pk(self, pk):
        self.__pk = pk

    @property
    def company_name(self):
        return self.__company_name

    @company_name.setter
    def company_name(self, company_name):
        self.__company_name = company_name
