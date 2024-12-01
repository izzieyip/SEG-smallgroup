'''Tests of the create_booking_request view'''
from django.test import TestCase
from django.urls import reverse
from tutorials.forms import Booking_requests
from tutorials.models import Booking_requests, User

class createBookingRequestViewTestCase(TestCase):
    """ Tests of the create booking requests view """

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('booking_request')
        self.student = User.objects.get(username='@johndoe')
        self.formInput = {
            "student" : self.student,
            "subject" : "DJ",
            "difficulty" : 1
        }

    def test_booking_request_url(self):
        self.assertEqual(self.url, '/request_booking/')

    def test_get_booking_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_booking_requests.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, Booking_requests))
        self.assertFalse(form.is_bound)

    def test_request_stored_successfully(self):
        before_count = Booking_requests.objects.count()
        response = self.client.post(self.url, self.formInput, follow=True)
        after_count = Booking_requests.objects.count()
        self.assertEqual(after_count, before_count+1)