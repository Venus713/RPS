from mpc.Payment import Payment
from mpc.Quote import Quote


class Method():

    def __init__(self, payment: Payment, quote: Quote):
        self.__payment = payment
        self.__quote = quote
        self.__payment.method = "banktransfer"

    @property
    def quote(self):
        return self.__quote

    def amount_outstanding(self):
        return self.quote.total()

    def get_data(self):
        print("\n*****************\nEFT GET DATA\n*****************\n")
        return self.__payment.get_data()

    def capture(self):
        print("Outstanding: ", self.amount_outstanding())
        return True