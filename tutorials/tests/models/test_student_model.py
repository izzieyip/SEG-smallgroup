''' Unit tests for the Student model.'''

from django.core.exceptions import ValidationError
from django.test import TestCase
from tutorials.models import Student



def _assert_student_is_valid(self):
    try:
        self.user.full_clean()
    except (ValidationError):
        self.fail('Test user should be valid')

def _assert_tutor_is_invalid(self):
    with self.assertRaises(ValidationError):
        self.user.full_clean()

