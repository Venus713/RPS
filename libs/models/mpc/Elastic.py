import requests


class Elastic():
    def __init__(self, host='localhost:9200', index_name='mpc-products-v8', doc_type='products', awsauth=None):
        self.__host = host
        self.__index_name = index_name
        self.__doc_type = doc_type
        self.__awsauth = awsauth

    @property
    def search_url(self):
        if self.__awsauth:
            return 'https://' + self.__host + '/' + self.__index_name + '/_search'
        else:
            return 'http://' + self.__host + '/' + self.__index_name + '/_search'

    @property
    def index_url(self):
        if self.__awsauth:
            return 'https://' + self.__host + '/' + self.__index_name + '/' + self.__doc_type
        else:
            return 'http://' + self.__host + '/' + self.__index_name + '/' + self.__doc_type

    def post_search(self, query):
        headers = {"Content-Type": "application/json"}

        if self.__awsauth:
            return requests.post(self.search_url, json=query, headers=headers, auth=self.__awsauth)
        else:
            return requests.post(self.search_url, json=query, headers=headers)
