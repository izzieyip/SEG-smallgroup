from django.test import TestCase, Client
from django.urls import reverse
from tutorials.models import Student

# this test code was also make with help from generative ai

class StudentDashboardViewTests(TestCase):
    def setUp(self):
        # Create a test student user
        self.user = Student.objects.create(username='@student_user', password='Password123', first_name='Lisa', last_name='Rose', email='lisa.rose@gmail.com')
        self.client = Client()
        self.url = reverse('student_dashboard')

    def test_student_dashboard_view_renders(self):
        """Test that the student dashboard renders successfully."""
        self.client.login(username='@student_user', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')

    def test_student_dashboard_contains_correct_content(self):
        """Test that the dashboard shows the correct content for a student."""
        self.client.login(username='@student_user', password='Password123')
        response = self.client.get(self.url)
        self.assertContains(response, f"Welcome to your dashboard {self.user.username}")
        self.assertContains(response, "View my Lessons")
        self.assertContains(response, "Lesson Payments")
        self.assertContains(response, "Book New Lessons")
        self.assertContains(response, "Good luck studying :)")

    def test_student_dashboard_links_resolve(self):
        """Test that all student dashboard links resolve correctly."""
        self.client.login(username='@student_user', password='Password123')

        # Reverse URLs for student actions
        my_bookings_url = reverse('my_bookings')
        my_payments_url = reverse('my_payments')
        create_booking_requests_url = reverse('create_booking_requests')

        # Check if the URLs are accessible
        self.assertEqual(self.client.get(my_bookings_url).status_code, 200)
        self.assertEqual(self.client.get(my_payments_url).status_code, 200)
        self.assertEqual(self.client.get(create_booking_requests_url).status_code, 200)
