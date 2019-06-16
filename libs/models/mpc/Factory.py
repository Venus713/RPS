from . import Customer
from . import Product
from . import Address
from . import Payment
from . import Quote
from . import Order
from .PaymentMethod import Eft as EftPayment
from .Config import Config


class Factory:

    def __init__(self, dydb=None):
        self.__dydb = dydb

    def order_from_quote(self, quote: Quote, user_id):
        order = Order.Order(dydb=self.__dydb, cognito_id=user_id)
        order.init_from_quote(quote)
        return order

    def new_payment(self, quote: Quote.Quote):

        print("Quote Currency : ", quote.currency)
        print("Quote Currency Rate: ", quote.currency_rate)
        # quote.currency
        pmt = Payment.Payment(dydb=self.__dydb,
                              amount=quote.total,
                              shipping_amount=quote.shipping_amount,
                              order_number=quote.order_number,
                              rate=quote.currency_rate
                              )
        pmt.method = quote.payment_method

        if quote.payment_method == "banktransfer":
            eft = EftPayment.Eft()
            pmt.action = eft

        return pmt

    def new_customer(self):
        return self.make("Customer")  # type: Customer

    def load_customer(self, pk):
        customer = Customer.Customer(dydb=self.__dydb)
        customer.load(pk)
        return customer

    def new_product(self):
        return self.make("Product")  # type: Product

    def new_billing_address(self, customer: Customer):
        address = self.make("BillingAddress")  # type: Address
        address.sk = "ADDRESS#BILLING#{}".format(address.pk)
        address.pk = customer.pk
        address.customer_pk = customer.pk
        return address

    def new_shipping_address(self, customer: Customer):
        address = self.make("ShippingAddress")  # type: Address
        address.sk = "ADDRESS#SHIPPING#{}".format(address.pk)
        address.pk = customer.pk
        address.customer_pk = customer.pk
        return address

    def make(self, model):
        if model == "Product":
            return Product.Product(dydb=self.__dydb)

        if model == "Customer":
            return Customer.Customer(dydb=self.__dydb)

        if model == "Address":
            address = Address.Address(dydb=self.__dydb)
            address.pk = address.new_guid()
            address.sk = "ADDRESS"
            return address

        if model == "ShippingAddress":
            address = Address.Address(dydb=self.__dydb)
            address.pk = address.new_guid()
            address.type = "shipping"
            address.sk = "ADDRESS#SHIPPING"
            return address

        if model == "BillingAddress":
            address = Address.Address(dydb=self.__dydb)
            address.pk = address.new_guid()
            address.type = "billing"
            address.sk = "ADDRESS#BILLING"
            return address
