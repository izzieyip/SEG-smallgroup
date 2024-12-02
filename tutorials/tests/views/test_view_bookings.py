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
        #Page setup with superuser login
        self.url = reverse('view_bookings')
        self.user = User.objects.get(username='@johndoe') #NEEDS TO BE A SUPERUSER ONCE THE SUPERUSER CHECK IS IN PLACE

    ''' below is actually needed for the create booking form stuff but ill leave it for now just in case
        #Generate sample data for Student and Tutor
        self.student = Student.objects.create(
            username = "@jamesstudent",
            first_name="James", 
            last_name="Student", 
            email="jamesstudent@example.com", 
            skill_to_learn="DJ",
            difficulty_level="1"
        )
        self.tutor = Tutor.objects.create(
            username = "@professordoe",
            first_name="Professor", 
            last_name="Doe",
            email="profdoe@example.com", 
            skills="DJ",
            experience_level="5"
        )

        #Generate sample Booking Request
        self.booking_request = Booking_requests.objects.create(
            student=self.student,
            subject="DJ",
            isConfirmed=False
        )

        #Generate sample Confirmed Booking
        self.confirmed_booking = Confirmed_booking.objects.create(
            booking=self.booking_request,
            tutor=self.tutor,
            booking_date=date(2024, 12, 25),
            booking_time=time(12, 30)
        )'''

    def test_view_bookings_url(self):
        self.assertEqual(self.url,'/view_bookings/')

    def test_get_view_bookings(self):
        self.client.login(username=self.user.username, password='Password123') #NEEDS TO BE A SUPERUSER ^
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_bookings.html')

    def test_get_view_bookings_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)