"""Unit tests of the sign up form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from tutorials.forms import SignUpForm
from tutorials.models import User, Tutor

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    def setUp(self):
        # data to test that the sign up form works for students
        self.form_input_student = { 
            'userType' : 'S',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        # data to test that the sign up form works for tutors
        self.form_input_tutor = {
            'userType' : 'T',
            'first_name': 'Petra',
            'last_name': 'Doe',
            'username': '@petradoe',
            'email': 'petradoe@example.org',
            'new_password': '123Password',
            'password_confirmation': '123Password',
            'skills' : "PY",
            'experience_level' : 4,
            'available_days' : "MON",
            'available_times' : 1

        }


    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input_student)
        form_tutor = SignUpForm(data = self.form_input_tutor)
        self.assertTrue(form.is_valid())
        self.assertTrue(form_tutor.is_valid())


    def test_student_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('userType', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_tutor_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('userType', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))
        #self.assertIn('skills', form.fields)


    def test_form_uses_model_validation(self):
        self.form_input_student['username'] = 'badusername'
        form = SignUpForm(data=self.form_input_student)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input_student['new_password'] = 'password123'
        self.form_input_student['password_confirmation'] = 'password123'
        form = SignUpForm(data=self.form_input_student)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input_student['new_password'] = 'PASSWORD123'
        self.form_input_student['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input_student)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input_student['new_password'] = 'PasswordABC'
        self.form_input_student['password_confirmation'] = 'PasswordABC'
        form = SignUpForm(data=self.form_input_student)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input_student['password_confirmation'] = 'WrongPassword123'
        form = SignUpForm(data=self.form_input_student)
        self.assertFalse(form.is_valid())


    def test_student_form_must_save_correctly(self):
        form = SignUpForm(data=self.form_input_student)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = User.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)

    def test_tutor_form_must_save_correctly(self):
        form = SignUpForm(data=self.form_input_tutor)
        before_count = Tutor.objects.count()
        form.save()
        after_count = Tutor.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = Tutor.objects.get(username='@petradoe')
        self.assertEqual(user.first_name, 'Petra')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'petradoe@example.org')
        is_password_correct = check_password('123Password', user.password)
        self.assertTrue(is_password_correct)
        self.assertEqual(user.skills, 'PY')
        self.assertEqual(user.experience_level, 4)
        self.assertEqual(user.available_days, 'MON')
        self.assertEqual(user.available_times, 1)
