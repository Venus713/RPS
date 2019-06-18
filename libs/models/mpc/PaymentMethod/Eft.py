from libs.models.mpc.Payment import Payment
from libs.models.mpc.Quote import Quote
import simplejson as json

class Eft():

    def __init__(self):
        self.__name = "banktransfer"

    def __str__(self):
        return self.__name

    @property
    def name(self):
        return self.__name

    def get_data(self):
        return {
            "name": self.__name
        }
