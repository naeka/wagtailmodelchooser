import decimal
import random

from django.urls import reverse
from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from . import models


class TestItemChooserView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    def test_simple(self):
        response = self.client.get(reverse('item_chooser'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailmodelchooser/chooser/model_chooser.html')
        self.assertTemplateUsed(response, 'wagtailmodelchooser/chooser/model_chooser.js')

    def test_search(self):
        response = self.client.get(reverse('item_chooser'), {'q': "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['query_string'], "Hello")

    def make_items(self):
        for i in range(50):
            models.Item.objects.create(
                title="Test {}".format(i),
                price=decimal.Decimal(random.randrange(10000)) / 100,
                stock_quantity=random.randrange(100)
            )

    def test_pagination(self):
        self.make_items()

        response = self.client.get(reverse('item_chooser'), {'p': 2})

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailmodelchooser/models/list.html')

        # Check that we got the correct page
        self.assertEqual(response.context['object_list'].number, 2)

    def test_pagination_invalid(self):
        self.make_items()

        response = self.client.get(reverse('item_chooser'), {'p': 'Hello World!'})

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailmodelchooser/models/list.html')

        # Check that we got page one
        self.assertEqual(response.context['object_list'].number, 1)

    def test_pagination_out_of_range(self):
        self.make_items()

        response = self.client.get(reverse('item_chooser'), {'p': 99999})

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailmodelchooser/models/list.html')

        # Check that we got the last page
        self.assertEqual(response.context['object_list'].number, response.context['object_list'].paginator.num_pages)


class TestItemChooserChosenView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        # Create an item to choose
        self.item = models.Item.objects.create(
            title="Test item", price=decimal.Decimal('19.99'), stock_quantity=40)

    def test_simple(self):
        response = self.client.get(reverse('item_chosen', args=(self.item.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailmodelchooser/chooser/model_chosen.js')
        self.assertContains(response, '"title": "Test item"')
