"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models import Admin

class HomeViewTestCase(TestCase):
    """Tests of the home view."""

    def setUp(self):
        self.url = reverse('home')
        #Setup admin login 
        self.user = Admin.objects.create(
            username = "@AdminLogin",
            first_name="Admin", 
            last_name="Login", 
            email="adminlogin@example.com", 
            password="pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=",
        )

    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_home_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        print("Response status code:", response.status_code)
        print("Response content:", response.content.decode())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')