from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from segmentsconfigapp.parser import ParserSegmentConfig

# Create your tests here.
class AccountTests(APITestCase):
    def test_parsing(self):
        test_li = [("@product\n*/product/*\n\n@article\n*article.html\n@comments\n*/comments/*.html",True),#OK
                             ("@product\n\n\n@article\n*article.html\n@comments\n*/comments/*.html", False),#FAIL
                             ("@product\n*/product/*\n\n*article.html\n@comments\n*/comments/*.html", False),#FAIL
                             ("@product\n*/product/*", True),#OK
                             ("@product\n*/product/*\n@product\nproduct.html", False),#Fail
                             ]
        for test in test_li:
            p = ParserSegmentConfig()
            res = p.parse(test[0])
            p.debug_print()
            self.assertEqual(test[1], res)


    def test_check_url(self):
        data_default = {
            "name": "123",
            "rules_set": "@product\n*/product/*\n\n@article\n*article.html\n@comments\n*/comments/*.html",
        }
        data_url = [
            "http://www.amazon.com/product/iphone.html",
            "http://www.amazon.com/magazine/health/2990-article.html",
            "http://www.amazon.com/",
            "http/wwwamazoncom/"
        ]
        self.client.post("/segments_config/", data_default, format='json')
        response = self.client.post("/segments_config/123/check_urls", data_url, format='json')
        values = ["product", "article", "UNKNOWN", "NOT_VALID"]
        i = 0
        while i < len(values):
            self.assertEqual(values[i], response.data[i]["value"])
            i+=1

