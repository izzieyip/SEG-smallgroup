"""Tests for dashboard view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models import Admin, Student, Tutor
from tutorials.tests.helpers import reverse_with_next

class DashboardViewTests(TestCase):
    """Test suite for the dashboard view"""
    def setUp(self):
        self.admin = Admin.objects.create_user(
            username = "@AdminLogin",
            first_name="Admin", 
            last_name="Login", 
            email="adminlogin@example.com", 
            password="Hello1",
        )
        self.student = Student.objects.create_user(
            username = "@StudentLogin",
            first_name = 'Student',
            last_name = "Login",
            email="studentlogin@example.com",
            password="Hello1",
        )
        self.tutor = Tutor.objects.create_user(
            username = "@TutorLogin",
            first_name = 'Tutor',
            last_name = "Login",
            email="tutorlogin@example.com",
            password="Hello1",
            skills = "DJ",
            experience_level = 4,
            available_days = "MON",
            available_times = 3
        )
        self.adminURL = reverse('dashboard')
        self.studentURL = reverse('student_dashboard')
        self.tutorURL = reverse('tutor_dashboard')

    def test_admin_dashboard_url(self):
        self.assertEqual(self.adminURL, '/dashboard/')

    def test_student_dashboard_url(self):
        self.assertEqual(self.studentURL, '/student_dashboard/')
    
    def test_tutor_dashboard_url(self):
        self.assertEqual(self.tutorURL, '/tutor_dashboard/')

    def test_get_admin_dashboard(self):
        self.client.login(username=self.admin.username, password='Hello1')
        response = self.client.get(self.adminURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_student_dashboard(self):
        self.client.login(username=self.student.username, password='Hello1')
        response = self.client.get(self.studentURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')

    def test_get_tutor_dashboard(self):
        self.client.login(username=self.tutor.username, password='Hello1')
        response = self.client.get(self.tutorURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor_dashboard.html')

    def test_get_admin_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.adminURL)
        response = self.client.get(self.adminURL)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_student_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.studentURL)
        response = self.client.get(self.studentURL)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_tutor_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.tutorURL)
        response = self.client.get(self.tutorURL)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)