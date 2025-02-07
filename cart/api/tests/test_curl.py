import requests
import json
import pprint
from django.test import TestCase

from api.requests import make_request
from api.requests import make_request_with_session


URL_CART = "http://127.0.0.1:8000/api/v1/"
PATH_CART = "cart/"
PATH_ADD_TO_CART = "cart/items/"


class CartDetailCurlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = requests.Session()
    
    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_cart_detail_handles_empty_cart(self):
        example_date = {
            "items": {},
            "total_quantity": 0,
            "total_price": 0.0,
        }

        data = self._get_cart()
        self._check_expected_keys_and_types(data)

        self.assertEqual(data, example_date)

    def _check_expected_keys_and_types(self, data):
        expected_data = {
            "items":            dict,
            "total_quantity":   int,
            "total_price":      float,
        }

        for key, value_type in expected_data.items():
            self.assertIn(key, data)
            self.assertIsInstance(data[key], value_type)

    def _get_cart(self):
        response = self.session.get(URL_CART+PATH_CART)

        try:
            data = response.json()
        except json.JSONDecodeError:
            print("JSON decoding Error.")
            data = dict()
        
        self.assertEqual(response.status_code, 200)

        return data 

    def _get_products_from_catalog(self):
        status, products = make_request(method="GET", host="127.0.0.1", port=8001, endpoint=f"/api/v1/", return_status=True) 

        self.assertEqual(status, 200)

        return products

    def _format_cart_data(self, products, payload):
        temp_products_data = {}
        for product in products["products"]:
            temp_products_data.update({
                str(product["id"]): {
                    "product": product,
                    "quantity": payload['quantity'],
                    "price": product['price'],
                    "total_price": product['price'] * payload['quantity'],
                }
            })

        example_data = {
            "items": temp_products_data,
            "total_quantity": sum(value["quantity"] for value in temp_products_data.values()),
            "total_price": sum(value['price'] * value['quantity'] for value in temp_products_data.values())
        }
        return example_data


class CartAddCurlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = requests.Session()
    
    @classmethod
    def tearDownClass(cls):
        cls.session.close()
    
    def test_successful_addition_an_item_to_cart(self):
        payload = {
            "product_id":   1,
            "quantity":     5,
            "override":     True,
        }
        url = URL_CART + PATH_ADD_TO_CART

        status, data = make_request_with_session(session=self.session, method="POST", payload=payload, url=url)

        self.assertEqual(status, 200)

    def test_check_return_result_when_adding_an_item_to_cart(self):
        pass

    def test_change_quantity_an_item_in_cart(self):
        pass

    def test_add_an_additional_quantity_an_item_to_cart(self):
        pass

