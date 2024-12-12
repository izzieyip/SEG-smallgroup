"""Tests of the view bookings view."""
from django.test import TestCase
from django.urls import reverse
from datetime import date, time
from tutorials.models import *
from tutorials.tests.helpers import reverse_with_next

class BookingViewTestCase(TestCase):
    """Tests of the view_bookings view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        #Setup admin login
        self.url = reverse('view_bookings')  + '?sortby=date' #to prevent redirect
        self.user = Admin.objects.create(
            username = "@AdminLogin",
            first_name="Admin", 
            last_name="Login", 
            email="adminlogin@example.com", 
            password="pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=",
        )
        #User.objects.get(username='@johndoe')

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

        #Generate 2 sample Booking Requests to test sorting
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

    def test_view_bookings_url(self):
        self.assertEqual(self.url, '/view_bookings/?sortby=date')

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
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('view_bookings'), {'sortby':'date', 'filterby':'student', 'search':'James'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'James Student')

    def test_valid_filtering_without_result(self):
        self.client.login(username=self.user.username, password='Password123')
        #makes confirmed_booking not appear
        response = self.client.get(reverse('view_bookings'), {'sortby':'date', 'filterby':'difficulty', 'search':'5'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'James Student')

    def test_default_sorting(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('view_bookings'), {'sortby':'date'}) #booking 1 should come before 2
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DJ') #order matters
        self.assertContains(response, 'PY')

    def test_custom_sorting(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('view_bookings'), {'sortby':'time'}) #booking 2 should come before 1
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PY') #order matters
        self.assertContains(response, 'DJ')

    '''EDIT BUTTON TESTS GO HERE'''

    def test_delete_booking(self):
        self.client.login(username=self.user.username, password='Password123')
        bookingCountBefore = Confirmed_booking.objects.count()
        response = self.client.post(reverse('delete_booking', args=[self.confirmed_booking1.id]))
        self.assertEqual(response.status_code, 302) #test for redirect
        bookingCountAfter = Confirmed_booking.objects.count()
        self.assertEqual(bookingCountAfter, bookingCountBefore - 1)