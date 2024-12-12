"""Tests of the invoices view."""
from django.test import TestCase
from django.urls import reverse
from datetime import date, time
from tutorials.models import *
from tutorials.tests.helpers import reverse_with_next

class BookingViewTestCase(TestCase):
    """Tests of the invoices view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        #NEEDS NEW INVOICE MODEL TO FINISH, JUST GO THROUGH AND REPLACE STUFF WHEN DONE

        '''

        #Setup admin login
        self.url = reverse('invoices')  + '?sortby=year' #to prevent redirect
        self.user = Admin.objects.create(
            username = "@AdminLogin",
            first_name="Admin", 
            last_name="Login", 
            email="adminlogin@example.com", 
            password="pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=",
        )
        #User.objects.get(username='@johndoe')

        #Needs a sample invoice to test deleting it
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

        USE SIMILAR TESTS FROM MY_BOOKINGS
    
    '''