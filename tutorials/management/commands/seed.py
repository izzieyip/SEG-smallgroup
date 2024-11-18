from django.core.management.base import BaseCommand, CommandError

from tutorials.models import User, Student, Tutor

import pytz
from faker import Faker
import random

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 300
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    skills = [
    ("CPP", "C++"),
    ("JA", "JAVA"),
    ("PY", "PYTHON"),
    ("DJ", "DJANGO")
    ]

    difficulty_levels = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
    ]
    


    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        self.students = Student.objects.all()
        self.tutors = Tutor.objects.all()

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
       
    def try_create_user(self, data):
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )


########################################################################################################################

    def generate_random_users(self):
        student_count = Student.objects.count()
        while student_count < self.USER_COUNT:
            print(f"Seeding student {student_count}/{self.USER_COUNT}", end='\r')
            self.generate_student()
            student_count = Student.objects.count()

        #generate 300 tutors
        tutorcount = Tutor.objects.count()
        while tutorcount < self.USER_COUNT:
            print(f"Seeding tutor {tutorcount}/{self.USER_COUNT}", end='\r')
            self.generate_tutor()
            tutorcount = Tutor.objects.count()

        print("User seeding complete.      ")


    #STUDENT
    def generate_student(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        #student attributes
        num1 = random.randint(0,3)
        skill = self.skills[num1][0]
        num2 = random.randint(0,4)
        level = self.difficulty_levels[num2][0]

        self.try_create_student({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'skill_to_learn': skill, 'difficulty_level': level})
       
    def try_create_student(self, data):
        try:
            self.create_student(data)
        except:
            print("failed")
            pass

    def create_student(self, data):
        Student.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            skill_to_learn=data['skill_to_learn'],
            difficulty_level=data['difficulty_level'],
        )

    
    #TUTOR
    def generate_tutor(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        #tutor attributes
        num1 = random.randint(0,3)
        skill = self.skills[num1][0]
        num2 = random.randint(0,4)
        level = self.difficulty_levels[num2][0]

        self.try_create_tutor({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'skills': skill, 'experience_level': level})
       
    def try_create_tutor(self, data):
        try:
            self.create_tutor(data)
        except:
            pass

    def create_tutor(self, data):
        Tutor.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            skills=data['skills'],
            experience_level=data['experience_level'],
        )


def create_username(first_name, last_name):
        return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
        return first_name + '.' + last_name + '@example.org'
