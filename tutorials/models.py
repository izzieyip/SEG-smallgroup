from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)


    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)
    
Skills = {
        "CPP": "C++",
        "JA" : "JAVA",
        "PY" : "PYTHON",
        "DJ" : "DJANGO"
    }
days = {
        "SUN" : 'Sunday',
        "MON" : 'Monday',
        "TUE" : 'Tuesday',
        "WED" : 'Wednesday',
        "THU" : 'Thursday',
        "FRI" : 'Friday',
        "SAT" : 'Saturday'
    }

times = {
    1 : "Morning",
    2 : "Afternoon",
    3 : "Evening",
    4 : "Morning and Afternoon",
    5 : "Afternoon and Evening",
    6 : "Morning and Evening",
    7 : "Whole day"
}

DIFFICULTY_LEVELS = [1, 2, 3, 4, 5]

class Student(User):
    skill_to_learn = models.CharField(choices = Skills, max_length= 3)
    difficulty_level = models.IntegerField(choices= DIFFICULTY_LEVELS)

    def __str__(self) -> str:
        return super().__str__() + f'wants to learn {self.skill_to_learn} at difficulty level {self.difficulty_level}'

class Tutor(User):
    skills = models.CharField(choices = Skills, max_length= 3)
    experience_level = models.IntegerField(choices= DIFFICULTY_LEVELS)

    def __str__(self) -> str:
        return super().__str__() + f'knows {self.skill_to_learn} with an experience level of {self.difficulty_level}'


class Availability(models.Model):
    tutor_id = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    available_day = models.CharField(choices=days, max_length=3)
    available_time = models.IntegerField(choices=times, max_length=1)

    def __str__(self) -> str:
        return f'{self.tutor_id.first_name} is available at {self.available_day} for the {self.available_time}'
