''' Unit tests for the Student model.'''

from django.core.exceptions import ValidationError
from django.test import TestCase
from tutorials.models import Student


class StudentModelTestCase(TestCase):

    def setUp(self):
        # Create sample data for testing
        self.skill = "DJANGO"
        self.difficulty_level = 2
        self.student = Student.objects.create(skill_to_learn = self.skill, difficulty_level = self.difficulty_level)

    def test_create_student(self):
        # Test creating an instance of student 
        student2 = Student.objects.create(skill_to_learn = self.skill, difficulty_level = self.difficulty_level)

        self.assertIsNotNone(student2.id)
        self.assertEqual(student2.skill, self.skill)
        self.assertEqual(student2.difficulty_level, self.difficulty_level)
        self._assert_student_is_valid()

    def test_student_str_method(self):
        # checking if the __str__ method works
        expected_str = super().__str__() + f'wants to learn {self.skill} at difficulty level {self.difficulty_level}'

        self.assertEquals(str(self.student), expected_str)

    def _assert_student_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_student_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

