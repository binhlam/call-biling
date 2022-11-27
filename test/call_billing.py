# -*- coding: utf-8 -*-
import json
import unittest
import requests

DOMAIN = "http://localhost:8000"
CALLING_ENPOINT = "/mobile/%s/call"
BILLING_ENDPOINT = "/mobile/%s/billing"


class RestCall:

    @classmethod
    def calling(cls, url, payload=None):
        try:
            r = requests.put(url, json=payload, headers={"Content-Type": "application/json"})
            r.raise_for_status()
            return r.status_code, json.loads(r.text)
        except requests.exceptions.Timeout as errt:
            print(errt)
            raise
        except requests.exceptions.HTTPError as errh:
            print(errh)
            raise
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            raise
        except requests.exceptions.RequestException as err:
            print(err)
            raise

    @classmethod
    def billing(cls, url):
        try:
            r = requests.get(url, headers={"Content-Type": "application/json"})
            r.raise_for_status()
            return r.status_code, json.loads(r.text)
        except requests.exceptions.Timeout as errt:
            print(errt)
            raise
        except requests.exceptions.HTTPError as errh:
            print(errh)
            raise
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            raise
        except requests.exceptions.RequestException as err:
            print(err)
            raise


class TestRESTMethods(unittest.TestCase):

    def test_calling_ok(self):
        with open("test/test_data.json", "r") as file:
            test_data = json.load(file)

        url = "%s%s" % (DOMAIN, (CALLING_ENPOINT % test_data["valid_user"]))
        code, data = RestCall.calling(url, {'call_duration': 3000})
        self.assertEqual(200, code)
        self.assertEqual(1, data['is_success'])

    def test_calling_fail(self):
        with open("test/test_data.json", "r") as file:
            test_data = json.load(file)

        url = "%s%s" % (DOMAIN, (CALLING_ENPOINT % test_data["invalid_user"]))  # exceeds max_length characters
        code, data = RestCall.calling(url, {'call_duration': 3000})
        self.assertEqual(200, code)
        self.assertEqual(0, data['is_success'])

    def test_billing_ok(self):
        with open("test/test_data.json", "r") as file:
            test_data = json.load(file)

        url = "%s%s" % (DOMAIN, (BILLING_ENDPOINT % test_data["valid_user"]))
        code, data = RestCall.billing(url)
        self.assertEqual(200, code)
        self.assertEqual(1, data['is_success'])

    def test_billing_fail(self):
        with open("test/test_data.json", "r") as file:
            test_data = json.load(file)

        url = "%s%s" % (DOMAIN, (BILLING_ENDPOINT % test_data["invalid_user"]))  # exceeds max_length characters
        code, data = RestCall.billing(url)
        self.assertEqual(200, code)
        self.assertEqual(0, data['is_success'])


if __name__ == "__main__":
    unittest.main()
