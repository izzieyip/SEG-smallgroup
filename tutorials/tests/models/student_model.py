"""Unit tests for the Student model."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from tutorials.models import User

class StudentModelTestCase(TestCase):
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()