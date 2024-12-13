from django.test import TestCase, Client
from django.urls import reverse
from tutorials.models import Admin


# this test code was made with help from generative AI

class AdminDashboardViewTests(TestCase):
    def setUp(self):
        # Create a test admin user
        self.user = Admin.objects.create(username='@admin_user', password='Password123', is_staff=False, first_name='Boo', last_name='Hoo', email='admin.best@gmail.com')
        self.client = Client()
        self.url = reverse('dashboard')

    def test_dashboard_view_renders(self):
        """Test that the dashboard renders successfully."""
        self.client.login(username='@admin_user', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')

    def test_dashboard_contains_correct_content(self):
        """Test that the dashboard shows the correct welcome message and links."""
        self.client.login(username='@admin_user', password='Password123')
        response = self.client.get(self.url)
        self.assertContains(response, f"Welcome to your dashboard {self.user.username}")
        self.assertContains(response, "View all Bookings")
        self.assertContains(response, "Create New Admin User")
        self.assertContains(response, "View Invoices")
        self.assertContains(response, "Manage all Users")

    def test_dashboard_links_resolve(self):
        """Test that all dashboard links resolve to correct URLs."""
        self.client.login(username='@admin_user', password='Password123')

        # Check that the URLs are properly reversed and accessible
        view_bookings_url = reverse('view_bookings')
        view_requests_url = reverse('view_requests')
        create_new_admin_url = reverse('create_new_admin')
        invoices_url = reverse('invoices')
        view_users_url = reverse('view_users')
        create_booking_url = reverse('create_booking')

        # Make sure the links work
        self.assertEqual(self.client.get(view_bookings_url).status_code, 200)
        self.assertEqual(self.client.get(view_requests_url).status_code, 200)
        self.assertEqual(self.client.get(create_new_admin_url).status_code, 200)
        self.assertEqual(self.client.get(invoices_url).status_code, 200)
        self.assertEqual(self.client.get(view_users_url).status_code, 200)
        self.assertEqual(self.client.get(create_booking_url).status_code, 200)
