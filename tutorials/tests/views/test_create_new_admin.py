from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tutorials.models import Admin
from tutorials.tests.helpers import reverse_with_next

class CreateAdminUserViewTestCase(TestCase):
    """Tests for creating a new admin user."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        # Set up the admin login and the URL to create a new admin user
        self.url = reverse('create_new_admin')
        self.user = Admin.objects.create_user(
            username="@AdminLogin",
            first_name="Admin",
            last_name="Login",
            email="adminlogin@example.com",
            password="Password123",
        )
        self.data_valid = {
            'username': '@newadmin',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'first_name': 'New',
            'last_name': 'Admin',
            'email': 'new.admin@example.com',
        }
        self.data_invalid = {
            'username': '',  # Empty username
            'password1': 'pass',  # Password too short
            'password2': 'passsdhlasj',  # Passwords don't match
            'email': 'invalid-email',  # Invalid email format
        }

    def test_create_admin_url(self):
        """Test the URL for creating a new admin."""
        self.assertEqual(self.url, '/create_new_admin/')

    def test_get_create_admin_form(self):
        """Test that the form for creating a new admin user renders successfully."""
        self.client.login(username='@AdminLogin', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_new_admin.html')
        self.assertContains(response, '<form')  # Check if the form tag is present.
        self.assertContains(response, 'Create Admin User')  # Check for the submit button text.

    # we have already tests that it creates a new user properly in the forms test

    def test_create_admin_user_invalid_post(self):
        count = Admin.objects.count()
        """Test that posting invalid data does not create a new admin user."""
        self.client.login(username='@AdminLogin', password='Password123')
        response = self.client.post(self.url, self.data_invalid)
        self.assertEqual(response.status_code, 200)  # Stay on the page due to form errors.
        self.assertContains(response, 'This field is required')  # Example error message.
        self.assertEqual(Admin.objects.count(),  count)  # No admin should be created.

    def test_create_admin_requires_login(self):
        """Test that accessing the page without login redirects to the login page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('log_in')))
