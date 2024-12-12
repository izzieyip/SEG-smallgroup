"""Unit tests for the Tutor model."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from tutorials.models import Tutor

class TutorModelTestCase(TestCase):

    # converting all lists of tuples to dictionaries to be able to access a value using its key
    skillsList = dict([
    ("CPP", "C++"),
    ("JA", "Java"),
    ("PY", "Python"),
    ("DJ", "Django")
    ])

    days = dict([
        ("SUN", 'Sunday'),
        ("MON", 'Monday'),
        ("TUE", 'Tuesday'),
        ("WED", 'Wednesday'),
        ("THU", 'Thursday'),
        ("FRI", 'Friday'),
        ("SAT", 'Saturday')
    ])

    times = dict([
        (1, "Morning"),
        (2, "Afternoon"),
        (3, "Evening"),
        (4, "Morning and Afternoon"),
        (5, "Afternoon and Evening"),
        (6, "Morning and Evening"),
        (7, "Whole day")
    ])

    difficulty_levels = dict([
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    ])

    def setUp(self):
        # Create sample data for testing
        self.firstName = "Peter"
        self.lastName = "Pickles"
        self.username = "@peterpickles"
        self.email = "peterpickles@example.org"
        self.password = "pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc="
        self.skills = "PY"
        self.experience_level = 4
        self.available_day = "MON"
        self.available_time = 7
        self.tutor = Tutor.objects.create(first_name = self.firstName, last_name = self.lastName, email = self.email, username = self.username, password = self.password, skills = self.skills, experience_level = self.experience_level, available_days = self.available_day, available_times = self.available_time)

    def test_create_tutor(self):
        # Test creating an instance of tutor 
        tutor2 = Tutor.objects.create(skills = self.skills, experience_level = self.experience_level, available_days = self.available_day, available_times = self.available_time)

        self.assertIsNotNone(tutor2.id)
        self.assertEqual(tutor2.skills, self.skills)
        self.assertEqual(tutor2.experience_level, self.experience_level)
        self.assertEqual(tutor2.available_days, self.available_day)
        self.assertEqual(tutor2.available_times, self.available_time)
        self._assert_tutor_is_valid()

    def test_tutor_str_method(self):
        # checking if the __str__ method works
        expected_str = f'{self.username} knows {self.skillsList[self.skills]} with an experience level of {self.experience_level} and is available on {self.days[self.available_day]} {self.times[self.available_time]}'
        self.assertEqual(str(self.tutor), expected_str)

    def test_skills_is_in_list(self):
        # testing when skill is in the list of skills
        self.tutor.skills = "JA"
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

    def test_available_day_in_list(self):
        # testing when available day is in the list
        self.tutor.available_days = "SAT"
        self._assert_tutor_is_valid()

    def test_avaiable_day_not_in_list(self):
        # testing when available day is not in the list
        self.tutor.available_days = "CAT"
        self._assert_tutor_is_invalid()

    def test_available_day_is_blank(self):
        # testing when available day is blank
        self.tutor.available_days = ""
        self._assert_tutor_is_invalid()

    def test_available_time_in_list(self):
        # testing when available time is in the list
        self.tutor.available_times = 3
        self._assert_tutor_is_valid()

    def test_available_time_not_in_list(self):
        # testing when available time is not in the list
        self.tutor.available_days = 21
        self._assert_tutor_is_invalid()

    def test_available_time_is_blank(self):
        # testing when available time is blank
        self.tutor.available_days = None
        self._assert_tutor_is_invalid()
   
    def _assert_tutor_is_valid(self):
        try:
            self.tutor.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_tutor_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.tutor.full_clean()