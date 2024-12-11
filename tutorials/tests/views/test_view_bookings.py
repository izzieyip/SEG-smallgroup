"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from datetime import date, time
from tutorials.models import *
from tutorials.tests.helpers import reverse_with_next

class BookingViewTestCase(TestCase):
    """Tests of the view_bookings view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        #Setup with superuser login
        self.url = reverse('view_bookings')
        self.user = User.objects.get(username='@johndoe')

        '''Needs a sample booking to test deleting it'''
        #Generate sample data for Student and Tutor
        self.student = Student.objects.create(
            username = "@Jamesstudent",
            first_name="James", 
            last_name="Student", 
            email="jamesstudent@example.com", 
        )
        self.tutor = Tutor.objects.create(
            username = "@professordoe",
            first_name="Professor", 
            last_name="Doe",
            email="profdoe@example.com", 
            skills="DJ",
            experience_level="3"
        )

        #Generate sample Booking Request
        self.booking_request = Booking_requests.objects.create(
            student=self.student,
            subject="DJ",
            difficulty=3,
            isConfirmed=False
        )

        #Generate sample Confirmed Booking
        self.confirmed_booking = Confirmed_booking.objects.create(
            booking=self.booking_request,
            tutor=self.tutor,
            booking_date=date(2024, 12, 25),
            booking_time=time(12, 30)
        )

    def test_view_bookings_url(self):
        self.assertEqual(self.url,'/view_bookings/')

    def test_get_view_bookings(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_bookings.html')

    def test_get_view_bookings_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_valid_filtering_with_result(self):
        #makes confirmed_booking not appear
        response = self.client.get(reverse('view_bookings'), {'sortby':'date', 'filterby':'difficulty', 'search':'5'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'James Student')

    #FIXTURES NOT WORKING ??

       