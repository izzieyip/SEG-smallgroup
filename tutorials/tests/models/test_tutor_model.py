"""Unit tests for the Tutor model."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from tutorials.models import Tutor

class TutorModelTestCase(TestCase):

    def setUp(self):
        # Create sample data for testing
        self.skills = "PYTHON"
        self.experience_level = 4
        self.tutor = Tutor.objects.create(skills = self.skills, experience_level = self.experience_level)

    def test_create_tutor(self):
        # Test creating an instance of tutor 
        tutor2 = Tutor.objects.create(skills = self.skills, experience_level = self.experience_level)

        self.assertIsNotNone(tutor2.id)
        self.assertEqual(tutor2.skills, self.skills)
        self.assertEqual(tutor2.experience_level, self.experience_level)
        self._assert_tutor_is_valid()

    def test_tutor_str_method(self):
        # checking if the __str__ method works
        expected_str = super().__str__() + f'knows {self.skills} with an experience level of {self.experience_level}'

        self.assertEquals(str(self.tutor), expected_str)

    def test_skills_is_in_list(self):
        # testing when skill is in the list of skills
        self.tutor.skills = "JAVA"
        self._assert_tutor_is_valid()

    def test_skills_not_in_list(self):
        # testing when skill is not in the list of skills
        self.tutor.skills = "CAT"
        self._assert_tutor_is_invalid()

    def test_skills_not_blank(self):
        # testing when skill field is left blank
        self.tutor.skills = " "
        self._assert_tutor_is_invalid()

    def test_experience_level_in_list(self):
        # testing when experience level is in the range 
        self.tutor.experience_level = "4"
        self._assert_tutor_is_valid()

    def test_experience_level_not_in_list(self):
        # testing when experience level is not in the range 
        self.tutor.experience_level = "10"
        self._assert_tutor_is_invalid()

    def test_experience_level_blank(self):
        # testing when the experience level is left blank
        self.tutor.experience_level = " "
        self._assert_tutor_is_invalid()

    def _assert_tutor_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_tutor_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()