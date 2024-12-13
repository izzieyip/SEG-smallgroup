# All these test have been written by AI
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.client import Client
from tutorials.models import Booking_requests, Student
from tutorials.forms import CreateBookingRequest

User = get_user_model()

class CreatingBookingRequestTests(TestCase):
    def setUp(self):
        # Create a user and a corresponding student instance
        self.user = Student.objects.create_user(username="@testuser", password="testpassword", first_name="Test", last_name="User", email="testuser@example.com")
        self.client = Client()
        self.url = reverse("create_booking_requests")  

    def test_get_request_renders_form(self):
        # Test if the GET request renders the form correctly
        self.client.login(username="@testuser", password="testpassword")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_booking_requests.html")
        self.assertIsInstance(response.context["form"], CreateBookingRequest)

    def test_post_request_creates_booking_request(self):
        # Test if a valid POST request creates a booking request
        self.client.login(username="@testuser", password="testpassword")
        post_data = {
            "subject": "PY",  # Replace with actual fields from your form
            "difficulty": 2,
        }

        response = self.client.post(self.url, data=post_data)

        # Check the redirection
        self.assertRedirects(response, reverse("dashboard"))

        # Check if the booking request is created
        self.assertTrue(Booking_requests.objects.filter(student=self.user).exists())

    def test_post_request_invalid_form(self):
        # Test if an invalid form does not create a booking request
        self.client.login(username="@testuser", password="testpassword")
        invalid_data = {
            "subject": "",  
            "difficulty": 2,
        }

        response = self.client.post(self.url, data=invalid_data)

        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertTemplateUsed(response, "create_booking_requests.html")
        self.assertFalse(Booking_requests.objects.filter(student=self.user).exists())

    def test_redirects_if_user_not_logged_in(self):
        # Test if unauthenticated users are redirected to the login page
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/log_in/?next={self.url}")
