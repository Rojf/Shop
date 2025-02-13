from decimal import Decimal

from django.conf import settings


class Cart:
    def __init__(self, request):
        """
        Initialize the bucket.

        :param request:
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {
                "items": {},
                "total_quantity": 0,
                "total_price": 0.0,
            }
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Adding an item to the cart or updating its quantity.

        :param product:
        :param quantity:
        :param override_quantity:
        :return:
        """
        product_id = str(product["id"])
        if product_id not in self.cart["items"]:
            self.cart["items"][product_id] = {
                "product": product,
                "quantity": 0,
                "price": product["price"],
            }

        if override_quantity:
            self.cart["items"][product_id]['quantity'] = quantity
        else:
            self.cart["items"][product_id]['quantity'] += quantity

        self.__add_total_price_for_product(self.cart["items"][product_id])
        self.__add_total_price_for_cart(self.cart)
        self.__add_total_quantity_for_cart(self.cart)

        self.session[settings.CART_SESSION_ID] = self.cart

        self.__save()

    def __save(self):
        # Mark the session as "modified"
        # to ensure that it is saved
        self.session.modified = True

    def remove(self, product_id):
        """
        Remove an item from the shopping cart

        :param product:
        :return:
        """
        product_id = str(product_id)
        if product_id in self.cart["items"]:
            del self.cart["items"][product_id]

        self.__add_total_price_for_cart(self.cart)
        self.__add_total_quantity_for_cart(self.cart)

        self.__save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.cart = {
            "items": {},
            "total_quantity": 0,
            "total_price": 0.0,
        }
        self.__save()

    def __add_total_price_for_product(self, item):
        item["total_price"] = float(Decimal(item['product']["price"] * item["quantity"]))

    def __add_total_quantity_for_cart(self, cart):
        cart["total_quantity"] = sum(
            item['quantity'] for item in self.cart["items"].values()
        )

    def __add_total_price_for_cart(self, cart):
        cart["total_price"] = float(
            sum(item['total_price'] for item in cart["items"].values())
        )

    def to_dict(self):
        items = {
            product_id: {
                "product": item["product"],
                "quantity": item["quantity"],
                "price": item["price"],
                "total_price": item["total_price"],
            }
            for product_id, item in self.cart["items"].items()
        }

        return {
            "items": items,
            "total_quantity": self.cart["total_quantity"],
            "total_price": self.cart["total_price"],
        }
