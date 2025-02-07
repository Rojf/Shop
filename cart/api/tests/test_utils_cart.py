from django.test import TestCase, RequestFactory, Client
from django.conf import settings
from unittest.mock import MagicMock
from api.cart import Cart


class CartTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.client = Client()
        session = self.client.session
        self.request.session = session
        self.cart = Cart(self.request)

        self.product_1 = {
            "id": "f4j0340j0fgj40",
            "price": 29,
            "name": "TriggerPoint Grid 1.0 Foam Roller",
            "image": "https://m.media-amazon.com/images/I/71Z7mW-76mL._AC_SX679_.jpg",
            "currency": "$",
        }

        self.product_2 = {
            "id": "fj02j43f02jfds",
            "price": 13.99,
            "name": "TriggerPoint Grid 1.0 Foam Roller",
            "image": "https://m.media-amazon.com/images/I/71Z7mW-76mL._AC_SX679_.jpg",
            "currency": "$",
        }


    def test_cart_initialization(self):
        self.assertEqual(
            self.cart.cart,
            {
                "items": {},
                "total_quantity": 0,
                "total_price": 0.0,
            }
        )

    def test_add_product(self):
        self.cart.add(self.product_1, quantity=3)
        product_id = str(self.product_1['id'])

        self.assertIn(product_id, self.cart.cart['items'])
        self.assertEqual(self.cart.cart['items'][product_id]['quantity'], 3)
        self.assertEqual(self.cart.cart['items'][product_id]['total_price'], 29*3)
        self.assertEqual(self.cart.cart['total_quantity'], 3)
        self.assertEqual(self.cart.cart['total_price'], 29*3)

    def test_override_quantity(self):
        self.cart.add(self.product_1, quantity=2)
        self.cart.add(self.product_1, quantity=1, override_quantity=True)
        product_id = str(self.product_1['id'])

        self.assertEqual(self.cart.cart['items'][product_id]['quantity'], 1)
        self.assertEqual(self.cart.cart['items'][product_id]['total_price'], 29)
        self.assertEqual(self.cart.cart['total_price'], 29)
        self.assertEqual(self.cart.cart['total_quantity'], 1)

    def test_remove_product(self):
        self.cart.add(self.product_1, quantity=3)
        product_id = str(self.product_1['id'])
        self.cart.remove(product_id)

        self.assertNotIn(product_id, self.cart.cart['items'])
        self.assertEqual(self.cart.cart['total_quantity'], 0)
        self.assertEqual(self.cart.cart['total_price'], 0.0)

    def test_clear_cart(self):
        self.cart.add(self.product_2, quantity=4)
        self.cart.add(self.product_1, quantity=2)
        self.cart.clear()

        self.assertEqual(
            self.cart.cart,
            {
                "items": {},
                "total_quantity": 0,
                "total_price": 0.0,
            }
        )

    def test_total_quantity_and_price(self):
        self.cart.add(self.product_1, quantity=3)
        self.cart.add(self.product_1, quantity=3)

        self.assertEqual(self.cart.cart['total_quantity'], 6)
        self.assertEqual(self.cart.cart['total_price'], 29 * 6)

    def test_to_dict(self):
        pass

