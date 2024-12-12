from django.test import TestCase
from django.urls import reverse
from tutorials.models import *
from tutorials.tests.helpers import reverse_with_next

class ViewUsersTestCase(TestCase):
    """Tests of the view_users view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        #Page setup with superuser login
        self.url = reverse('view_users')
        self.user = User.objects.get(username='@johndoe') 

    def test_view_users_url(self):
        self.assertEqual(self.url,'/view_users/')

    def test_get_view_users(self):
        self.client.login(username=self.user.username, password='Password123') 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_users.html')

    # this test is not working. 
    def test_get_view_users_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)