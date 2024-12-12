"""Tests of the my bookings view."""
from django.test import TestCase
from django.urls import reverse
from datetime import date, time
from tutorials.models import *
from tutorials.tests.helpers import reverse_with_next

class BookingViewTestCase(TestCase):
    """Tests of the my_bookings view for tutors."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        #URL FOR TUTOR
        self.url = reverse('my_bookings') + "?user=tutor"

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
            password="pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=",
            skills="DJ",
            experience_level="3"
        )
        self.othertutor = Tutor.objects.create(
            username = "@professordill",
            first_name="Professor", 
            last_name="Dill",
            email="profdill@example.com", 
            skills="PY",
            experience_level="2"
        )

        #Generate 3 sample Booking Requests to test sorting and invalid entries
        self.booking_request1 = Booking_requests.objects.create(
            student=self.student,
            subject="DJ",
            difficulty=3,
            isConfirmed=True
        )
        self.booking_request2 = Booking_requests.objects.create(
            student=self.student,
            subject="PY",
            difficulty=1,
            isConfirmed=True
        )
        self.booking_request3 = Booking_requests.objects.create(
            student=self.student,
            subject="JV",
            difficulty=2,
            isConfirmed=True
        )

        #Generate sample Confirmed Bookings
        self.confirmed_booking1 = Confirmed_booking.objects.create(
            booking=self.booking_request1,
            tutor=self.tutor,
            booking_date=date(2024, 12, 25),
            booking_time=time(11, 30)
        )
        self.confirmed_booking2 = Confirmed_booking.objects.create(
            booking=self.booking_request2,
            tutor=self.tutor,
            booking_date=date(2024, 12, 26),
            booking_time=time(10, 30)
        )
        self.confirmed_booking2 = Confirmed_booking.objects.create(
            booking=self.booking_request3,
            tutor=self.othertutor,
            booking_date=date(2024, 12, 27),
            booking_time=time(10, 31)
        )

    def test_my_bookings_url(self):
        self.assertEqual(self.url, '/my_bookings/?user=tutor')

    def test_get_my_bookings(self):
        self.client.login(username=self.tutor.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_bookings.html')

    def test_get_my_bookings_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200) 

    def test_correct_booking_display(self): #only bookings with this account should be shown
        self.client.login(username=self.tutor.username, password='Password123')
        response = self.client.get(reverse('my_bookings'), {'user':'tutor', 'sortby':'date'})
        self.assertNotContains(response, 'JV') #in booking3, which isnt for this user

    def test_default_sorting(self):
        self.client.login(username=self.tutor.username, password='Password123')
        response = self.client.get(reverse('my_bookings'), {'user':'tutor', 'sortby':'date'}) #booking 1 should come before 2
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DJ') #order matters
        self.assertContains(response, 'PY')

    def test_custom_sorting(self):
        self.client.login(username=self.tutor.username, password='Password123')
        response = self.client.get(reverse('my_bookings'), {'user':'tutor', 'sortby':'time'}) #booking 2 should come before 1
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PY') #order matters
        self.assertContains(response, 'DJ')