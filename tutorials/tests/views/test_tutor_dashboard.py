from django.test import TestCase, Client
from django.urls import reverse
from tutorials.models import Tutor

# this test code was made with help from generative ai

class TutorDashboardViewTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.firstName = "Bingo"
        self.lastName = "Card"
        self.username = "@bingocard"
        self.email = "bingocard@example.org"
        self.password = "Password123"
        self.skills = "PY"
        self.experience_level = 4
        self.available_day = "MON"
        self.available_time = 7
        self.tutor = Tutor.objects.create(first_name=self.firstName, last_name=self.lastName, email=self.email,
                                          username=self.username, password=self.password, skills=self.skills,
                                          experience_level=self.experience_level, available_days=self.available_day,
                                          available_times=self.available_time)

        self.client = Client()
        self.url = reverse('tutor_dashboard')

    def test_tutor_dashboard_renders_successfully(self):
        """Test that the tutor dashboard renders successfully."""
        self.client.login(username='@tutor_user', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor_dashboard.html')

    def test_tutor_dashboard_content(self):
        """Test that the tutor dashboard displays the correct dynamic and static content."""
        self.client.login(username='@tutor_user', password='Password123')
        response = self.client.get(self.url)

        # Check personalized greeting
        self.assertContains(response, f"Welcome to your dashboard {self.username}")
        self.assertContains(response, "Here you can check info on your students and see your scheduled lessons!")
        self.assertContains(response, "-- This is a tutor dashboard")

        # Check card titles and descriptions
        self.assertContains(response, "View my Schedule")
        self.assertContains(response, "Update my Skills")
        self.assertContains(response, "View my Students")
        self.assertContains(response, "Click here to view all my scheduled lessons")
        self.assertContains(response, "(not complete) Click here to update your tutoring skills")
        self.assertContains(response, "(not complete) Click here to see info on your assigned students")

    def test_tutor_dashboard_links(self):
        """Test that all links in the tutor dashboard resolve correctly."""
        self.client.login(username='@tutor_user', password='Password123')

        # Check the link for 'View my Schedule'
        my_bookings_url = reverse('my_bookings')  # Replace with the correct URL name for 'my_bookings'
        response = self.client.get(my_bookings_url)
        self.assertEqual(response.status_code, 200)

    def test_tutor_dashboard_placeholder_links(self):
        """Test that placeholder links do not cause errors."""
        self.client.login(username='@tutor_user', password='Password123')
        response = self.client.get(self.url)

        # Since placeholder links are '#', ensure they are not broken
        self.assertContains(response, 'href="#"')
