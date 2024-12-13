'''Tests of the create_booking_requests view'''
from django.test import TestCase
from django.urls import reverse
from tutorials.forms import Booking_requests
from tutorials.models import Student, User, Booking_requests

class createBookingRequestViewTestCase(TestCase):
    """ Tests of the create booking requests view """

    #fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_booking_requests')
        self.user = Student.objects.create(
            username = "@johndoe",
            first_name="John", 
            last_name="Doe", 
            email="johndoe@example.com", 
            password="pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=",
        )
        self.formInput = {
            "subject" : "DJ",
            "difficulty" : 1
        }

    def test_booking_request_url(self):
        self.assertEqual(self.url, '/dashboard/create_booking_requests/')

    def test_get_booking_request(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'create_booking_requests.html')

    def test_request_stored_successfully(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Booking_requests.objects.count()
        self.client.post(self.url, self.formInput, follow=True)
        after_count = Booking_requests.objects.count()
        self.assertEqual(after_count, before_count+1)
