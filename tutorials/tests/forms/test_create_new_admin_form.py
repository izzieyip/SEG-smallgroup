from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django import forms
from tutorials.forms import CreateNewAdminForm
from tutorials.models import User, Admin

## tests for the 'create a new admin form'
## first we test that the form contains the correct fields

class CreateNewAdminFormTestCase(TestCase):

    def setUp(self):
        # test data
        self.form_input = {
            'first_name': 'Ammu',
            'last_name': 'Bean',
            'username': '@AmmuBean',
            'email': 'ammubean@gmail.com',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }


    def test_create_new_admin_form_valid(self):
        form = CreateNewAdminForm(data = self.form_input)
        self.assertTrue(form.is_valid())


    def test_form_has_necessary_fields(self):
        form = CreateNewAdminForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('password_confirmation', form.fields)


    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = CreateNewAdminForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = CreateNewAdminForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = CreateNewAdminForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = CreateNewAdminForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['new_password'] = 'Password123'
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = CreateNewAdminForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_admin_form_must_save_correctly(self):
        form = CreateNewAdminForm(data=self.form_input)
        before_count = Admin.objects.count()
        form.save()
        after_count = Admin.objects.count()
        self.assertEqual(after_count, before_count+1)
        admin = Admin.objects.get(username='@AmmuBean')
        self.assertEqual(admin.first_name, 'Ammu')
        self.assertEqual(admin.last_name, 'Bean')
        self.assertEqual(admin.email, 'ammubean@gmail.com')
        is_password_correct = check_password('Password123', admin.new_password)
        self.assertTrue(is_password_correct)
