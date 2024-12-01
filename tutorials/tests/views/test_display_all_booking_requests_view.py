"""Tests of the display_all_booking_requests view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models import User

class Display_all_booking_requestsViewTestCase(TestCase):
    """Tests of the display_all_booking_requests view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('view_requests')
        self.user = User.objects.get(username='@johndoe')

    def test_view_requests_url(self):
        self.assertEqual(self.url,'/view_requests/')

    def test_get_view_requests(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_requests.html')

