from __future__ import absolute_import, unicode_literals

from random import randint
import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from . import models


class TestEventChooserView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    def test_simple(self):
        response = self.client.get(reverse('event_chooser'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtaileventchooser/chooser/event_chooser.html')
        self.assertTemplateUsed(response, 'wagtailmodelchooser/chooser/model_chooser.js')

    def test_search(self):
        response = self.client.get(reverse('event_chooser'), {'q': "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['query_string'], "Hello")

    def make_events(self):
        startdate = datetime.datetime(2010, 1, 1)
        for i in range(50):
            starts_on = startdate + datetime.timedelta(randint(1, 365 * 8))
            models.Event.objects.create(
                title="Test {}".format(i),
                starts_on=starts_on,
                ends_on=starts_on + datetime.timedelta(1, 14)
            )

    def test_pagination(self):
        self.make_events()

        response = self.client.get(reverse('event_chooser'), {'p': 2})

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtaileventchooser/events/list.html')

        # Check that we got the correct page
        self.assertEqual(response.context['object_list'].number, 2)

        # Check that custom columns are present
        self.assertContains(response, "<th>Starts on</th>")
        self.assertContains(response, "<th>Ends on</th>")

    def test_pagination_invalid(self):
        self.make_events()

        response = self.client.get(reverse('event_chooser'), {'p': 'Hello World!'})

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtaileventchooser/events/list.html')

        # Check that we got page one
        self.assertEqual(response.context['object_list'].number, 1)

    def test_pagination_out_of_range(self):
        self.make_events()

        response = self.client.get(reverse('event_chooser'), {'p': 99999})

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtaileventchooser/events/list.html')

        # Check that we got the last page
        self.assertEqual(response.context['object_list'].number, response.context['object_list'].paginator.num_pages)


class TestEventChooserChosenView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        # Create an event to choose
        self.event = models.Event.objects.create(
            title="Test event", starts_on=datetime.datetime(2016, 6, 20), ends_on=datetime.datetime(2016, 6, 21))

    def test_simple(self):
        response = self.client.get(reverse('event_chosen', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailmodelchooser/chooser/model_chosen.js')
        self.assertContains(response, '"title": "Test event"')
