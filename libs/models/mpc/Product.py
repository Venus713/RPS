from . import base


class Product(base.Base):
    def __init__(self,  dydb=None):
        super(Product, self).__init__(dydb)

    def get_product(self, sku):
        try:
            response = self.get_table().query(
                KeyConditionExpression="pk = :pk and sk = :sk",
                ExpressionAttributeValues={":pk": sku, ":sk": "PRODUCT"}
            )

            if list(response['Items']).__len__() > 0:
                return response['Items'][0]
            else:
                raise Exception("Unable to load product")
        except IndexError:

            return False

    def get_size(self, sku, size):
        single = None
        product = self.get_product(sku)
        images = product['images']

        if size in product['sizes']:
            single = product['sizes'][size]
            single.update({
                'sku': single['rs_simple_sku'],
                'name': product['product_name'],
                'images': images
            })
            del (single['status'])
            del (single['rs_simple_sku'])

            single.update(product['prices'])

        return single
