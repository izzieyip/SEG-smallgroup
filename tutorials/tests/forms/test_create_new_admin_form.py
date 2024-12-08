from django.test import TestCase

from tutorials.forms import CreateNewAdminForm

## tests for the 'create a new admin form'
## first we test that the form contains the correct fields

class CreateNewAdminFormTestCase(TestCase):
    def test_form_has_necessary_fields(self):
        form = CreateNewAdminForm()
        self.assertIn('username', form.fields)
        self.assertIn('firstname', form.fields)
        self.assertIn('lastname', form.fields)
        self.assertIn('password', form.fields)
        self.assertIn('email', form.fields)


    def test_create_new_admin_form_valid(self):
        form_input = {
            'firstname' : 'Ammu',
            'lastname' : 'Bean',
            'username' : '@AmmuBean',
            'email' : 'ammubean@gmail.com',
            'password' : 'Password123'
        }
        form = CreateNewAdminForm(data = form_input)
        self.assertTrue(form.is_valid())



