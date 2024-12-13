# these tests have been written by AI
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tutorials.models import Student, Tutor, Admin, User

class DisplayAllUsersViewTest(TestCase):

    def setUp(self):
        # Creating test data
        self.admin_user = Admin.objects.create_user(username='@admin', first_name='Admin', last_name='User', email='admin@example.com', password='password')
        self.student_user = Student.objects.create_user(username='@student', first_name='Student', last_name='User', email='student@example.com', password='password')
        self.tutor_user = Tutor.objects.create_user(username='@tutor', first_name='Tutor', last_name='User', email='tutor@example.com', password='password', skills='PY', experience_level=3, available_days='MON', available_times=1)

        self.url = reverse('view_users')  # Ensure this matches your URL pattern for displaying users

    def test_display_all_users_authenticated(self):
        # Login as admin
        self.client.login(username='@admin', password='password')

        # Send request and check response
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_users.html')

        # Check that context contains users, students, and tutors
        self.assertIn('admin', response.context)
        self.assertIn('students', response.context)
        self.assertIn('tutors', response.context)


    def test_display_all_users_not_authenticated(self):
        # Send request without logging in
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, '/log_in/?next=' + self.url)

class DeleteUserViewTest(TestCase):

    def setUp(self):
        self.admin_user = Admin.objects.create_user(username='@admin', first_name='Admin', last_name='User', email='admin@example.com', password='password')
        self.user_to_delete = User.objects.create_user(username='@delete_user', first_name='Delete', last_name='User', email='delete@example.com', password='password')

        self.delete_url = reverse('delete_user', kwargs={'id': self.user_to_delete.id})
        self.view_url = reverse('view_users')  # Ensure this matches your view URL

    def test_delete_user(self):
        # Login as admin
        self.client.login(username='@admin', password='password')

        # Send delete request
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        self.assertRedirects(response, self.view_url)

        # Verify that the user is deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='@delete_user')

    
class UpdateUserViewTest(TestCase):

    def setUp(self):
        self.admin_user = Admin.objects.create_user(username='@admin', first_name='Admin', last_name='User', email='admin@example.com', password='password')
        self.user_to_update = User.objects.create_user(username='@user_to_update', first_name='Old', last_name='User', email='olduser@example.com', password='password')

        self.update_url = reverse('update_user', kwargs={'user_id': self.user_to_update.id})

    def test_update_user(self):
        # Login as admin
        self.client.login(username='@admin', password='password')

        # Prepare data for the update
        new_data = {
            'username': '@updated_user',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updateduser@example.com'
        }

        # Send the POST request to update the user
        response = self.client.post(self.update_url, data=new_data)

        self.assertEqual(response.status_code, 302)  # Should redirect after update
        self.assertRedirects(response, reverse('view_users'))

        # Verify the user details were updated
        self.user_to_update.refresh_from_db()
        self.assertEqual(self.user_to_update.username, '@updated_user')
        self.assertEqual(self.user_to_update.first_name, 'Updated')
        self.assertEqual(self.user_to_update.last_name, 'User')
        self.assertEqual(self.user_to_update.email, 'updateduser@example.com')


    def test_update_user_not_found(self):
        # Login as admin
        self.client.login(username='@admin', password='password')

        # Test with a non-existent user ID
        non_existent_id = 9999
        update_url = reverse('update_user', kwargs={'user_id': non_existent_id})
        response = self.client.get(update_url)

        self.assertEqual(response.status_code, 404)  # Should raise Http404
