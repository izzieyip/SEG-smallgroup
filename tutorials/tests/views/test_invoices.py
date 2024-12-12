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
        #Setup admin login
        self.url = reverse('invoices')  + '?showpaid=false&sortby=year' #to prevent redirect
        self.user = Admin.objects.create(
            username = "@AdminLogin",
            first_name="Admin", 
            last_name="Login", 
            email="adminlogin@example.com", 
            password="pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=",
        )
        #User.objects.get(username='@johndoe')

        #Needs a sample invoice to test deleting it, requiring a booking and student/tutors
        #Generate sample data for Student and Tutor
        self.student1 = Student.objects.create(
            username = "@Jamesstudent",
            first_name="James", 
            last_name="Student", 
            email="jamesstudent@example.com", 
        )
        self.student2 = Student.objects.create(
            username = "@Stephstudent",
            first_name="Steph", 
            last_name="Student", 
            email="stephstudent@example.com", 
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
            student=self.student1,
            subject="DJ",
            difficulty=3,
            isConfirmed=True
        )
        self.booking_request2 = Booking_requests.objects.create(
            student=self.student2,
            subject="PY",
            difficulty=1,
            isConfirmed=True
        )

        #Generate sample Confirmed Bookings
        self.confirmed_booking1 = Confirmed_booking.objects.create(
            booking=self.booking_request1,
            tutor=self.tutor,
            booking_date=date(2022, 12, 25),
            booking_time=time(11, 30)
        )
        self.confirmed_booking2 = Confirmed_booking.objects.create(
            booking=self.booking_request2,
            tutor=self.tutor,
            booking_date=date(2023, 12, 26),
            booking_time=time(10, 30)
        )

        Invoices.objects.all().delete()

        #Generate invoices for both 
        self.invoice1 = Invoices.objects.create(
            booking=self.confirmed_booking1,
            student=self.student1,
            year=2022,
            amount=500,
            paid=False,
        )
        self.invoice2 = Invoices.objects.create(
            booking=self.confirmed_booking2,
            student=self.student2,
            year=2023,
            amount=100,
            paid=False,
        )

    def test_invoices_url(self):
        self.assertEqual(self.url, '/invoices/?showpaid=false&sortby=year')

    def test_get_invoices(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoices.html')

    def test_valid_filtering_with_result(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('invoices'), {'showpaid':'false', 'sortby':'year', 'filterby':'student', 'search':'James'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'James Student')
        self.assertNotContains(response, 'Steph Student')

    def test_valid_filtering_without_result(self):
        self.client.login(username=self.user.username, password='Password123')
        #makes confirmed_booking not appear
        response = self.client.get(reverse('invoices'), {'showpaid':'false', 'sortby':'year', 'filterby':'year', 'search':'2026'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'James Student')
        self.assertNotContains(response, 'Steph Student')

    def test_default_sorting(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('invoices'), {'showpaid':'false', 'sortby':'year'}) #booking 1 should come before 2
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2022') #order matters
        self.assertContains(response, '2023')

    def test_custom_sorting(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('invoices'), {'showpaid':'false', 'sortby':'amount'}) #booking 2 should come before 1
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2023') #order matters
        self.assertContains(response, '2022')

    def test_mark_as_paid(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(reverse('pay_invoice', args=[self.invoice1.id]))
        self.assertEqual(response.status_code, 302) #test for redirect

        #refresh page and data to test it
        response = self.client.get(reverse('invoices'), {'showpaid':'false', 'sortby':'year'})
        self.invoice1.refresh_from_db() #need to refresh invoice stuff
        self.assertEqual(self.invoice1.paid, True) #should be marked as true
        self.assertNotContains(response, '2022') #this invoice should no longer appear

    def test_mark_as_unpaid(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(reverse('unpay_invoice', args=[self.invoice1.id]))
        self.assertEqual(response.status_code, 302) #test for redirect

        #refresh page and data to test it
        response = self.client.get(reverse('invoices'), {'showpaid':'false', 'sortby':'year'})
        self.invoice1.refresh_from_db() #need to refresh invoice stuff
        self.assertEqual(self.invoice1.paid, False) #should be marked as true
        self.assertContains(response, '2022') #this invoice should no longer appear
