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
        self.url = reverse('my_payments') + "?sortby=year"

        #Generate sample data for Students
        self.student = Student.objects.create(
            username = "@Jamesstudent",
            first_name="James", 
            last_name="Student", 
            email="jamesstudent@example.com", 
            password="pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=",
        )
        self.otherstudent = Student.objects.create(
            username = "@Stephstudent",
            first_name="Steph", 
            last_name="Student", 
            email="Stephstudent@example.com", 
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
            student=self.otherstudent,
            subject="JV",
            difficulty=2,
            isConfirmed=True
        )

        #Generate invoices for both 
        self.invoice1 = Invoices.objects.create(
            booking=self.booking_request1,
            student=self.student,
            year=2021,
            amount=500,
            paid=False,
        )
        self.invoice2 = Invoices.objects.create(
            booking=self.booking_request2,
            student=self.student,
            year=2022,
            amount=200,
            paid=False,
        )
        self.invoice3 = Invoices.objects.create(
            booking=self.booking_request3,
            student=self.otherstudent,
            year=2023,
            amount=100,
            paid=False,
        )

    def test_my_payments_url(self):
        self.assertEqual(self.url, '/my_payments/?sortby=year')

    def test_get_my_payments(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_payments.html')

    def test_get_my_payments_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200) 

    def test_correct_booking_display(self): #only payments with this account should be shown
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(reverse('my_payments'), {'sortby':'year'})
        self.assertNotContains(response, '2023') #in booking3, which isnt for this user

    def test_default_sorting(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(reverse('my_payments'), {'sortby':'year'}) #booking 1 should come before 2
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2021') #order matters
        self.assertContains(response, '2022')

    def test_custom_sorting(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(reverse('my_payments'), {'sortby':'amount'}) #booking 2 should come before 1
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2022') #order matters
        self.assertContains(response, '2021')
    
    def test_show_no_invoices(self):
        self.client.login(username=self.student.username, password='Password123')
        Invoices.objects.all().delete()
        response = self.client.get(reverse('my_payments'), {'sortby':'year'})
        self.assertContains(response, 'All settled up!') #message should appear
