from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tutorials.models import Student, Tutor, Booking_requests, Confirmed_booking
from django.core.exceptions import ValidationError
from datetime import datetime

class CreateBookingTest(TestCase):

    def setUp(self):
        """Setup data for testing."""
        # Create a student user
        self.student = Student.objects.create_user(
            first_name='John', last_name='Doe', username='@studentuser', email='jd@gmail.com', password='Password123')
        
        # Create a tutor user
        self.tutor = Tutor.objects.create_user(
            first_name='Jane', last_name='Smith', username='@tutoruser', email='js@gmail.com', password='Password123', skills='DJ', experience_level=1, available_days='MON', available_times=6)
        
        # Create a booking request
        self.booking_request = Booking_requests.objects.create(
            student=self.student, subject='DJ', difficulty=1, isConfirmed=False
        )
        
        self.booking_url = reverse('create_booking')  

    def test_create_booking_success(self):
        """Test that a user can successfully create a booking."""
        self.client.login(username='studentuser', password='Password123')

        data = {
            'student': self.student.username,
            'subject': 'DJ',
            'date': '2024-05-01',
            'time': '10:00',
            'tutor': self.tutor.username,
        }

        response = self.client.post(self.booking_url, data)
        
        # Check that the booking was created
        booking = Confirmed_booking.objects.filter(tutor=self.tutor, booking=self.booking_request).first()
        self.assertIsNotNone(booking)
        self.assertEqual(response.status_code, 302)  # Assuming it redirects to a success page

    def test_create_booking_invalid_user(self):
        """Test that an error is raised if the user or tutor doesn't exist."""
        self.client.login(username='studentuser', password='Password123')

        data = {
            'booking': self.booking_request,
            'booking_date': '2024-05-01',
            'booking_time': '10:00',
            'tutor': 'invalidtutor',
        }

        response = self.client.post(self.booking_url, data)

        # Check that no booking was created and that an error message is displayed
        booking = Confirmed_booking.objects.filter(tutor=self.tutor, booking=self.booking_request).first()
        self.assertIsNone(booking)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)

    def test_create_booking_missing_fields(self):
        """Test that the form is invalid if some fields are missing."""
        self.client.login(username='studentuser', password='Password123')

        data = {
            'booking': self.booking_request,
            'booking_date': '2024-05-01',
            'tutor': 'invalidtutor',
        }

        response = self.client.post(self.booking_url, data)

        # Check if form errors appear for missing fields
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)

    def test_create_booking_invalid_date_format(self):
        """Test that the date format is correct."""
        self.client.login(username='studentuser', password='Password123')

        data = {
            'booking': self.booking_request,
            'booking_date': 'invalid',
            'booking_time': '10:00',
            'tutor': 'invalidtutor',
        }

        response = self.client.post(self.booking_url, data)

        # Ensure an error is raised due to invalid date format
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)

    def test_create_booking_invalid_time_format(self):
        """Test that the time format is correct."""
        self.client.login(username='studentuser', password='Password123')

        data = {
            'booking': self.booking_request,
            'booking_date': '2024-05-01',
            'booking_time': 'invalid',
            'tutor': 'invalidtutor',
        }

        response = self.client.post(self.booking_url, data)

        # Ensure an error is raised due to invalid time format
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
