from django.core.management.base import BaseCommand
from tutorials.models import User, Student, Tutor, Booking_requests, Confirmed_booking
import pytz
from faker import Faker
import random
import datetime

class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 300
    BOOKING_COUNT = 100
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    skills = [
        ("CPP", "C++"),
        ("JA", "Java"),
        ("PY", "Python"),
        ("DJ", "Django")
    ]

    difficulty_levels = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    available_days = [
        ("SUN", 'Sunday'),
        ("MON", 'Monday'),
        ("TUE", 'Tuesday'),
        ("WED", 'Wednesday'),
        ("THU", 'Thursday'),
        ("FRI", 'Friday'),
        ("SAT", 'Saturday')
    ]

    available_times = [
        (1, "Morning"),
        (2, "Afternoon"),
        (3, "Evening"),
        (4, "Morning and Afternoon"),
        (5, "Afternoon and Evening"),
        (6, "Morning and Evening"),
        (7, "Whole day")
    ]

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        self.students = Student.objects.all()
        self.tutors = Tutor.objects.all()
        self.create_bookings()
        print("Database seeded successfully!")

    def create_users(self):
        self.generate_random_users()

    def generate_random_users(self):
        student_count = Student.objects.count()
        while student_count < self.USER_COUNT:
            print(f"Seeding student {student_count}/{self.USER_COUNT}", end='\r')
            self.generate_student()
            student_count = Student.objects.count()

        tutor_count = Tutor.objects.count()
        while tutor_count < self.USER_COUNT:
            print(f"Seeding tutor {tutor_count}/{self.USER_COUNT}", end='\r')
            self.generate_tutor()
            tutor_count = Tutor.objects.count()

    # STUDENT
    def generate_student(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_student({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def try_create_student(self, data):
        try:
            self.create_student(data)
        except Exception as e:
            print(f"Failed to create student: {e}")

    def create_student(self, data):
        Student.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=self.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name']
        )

    # TUTOR
    def generate_tutor(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        skill = random.choice(self.skills)[0]
        level = random.choice(self.difficulty_levels)[0]
        day = random.choice(self.available_days)[0]
        time = random.choice(self.available_times)[0]

        self.try_create_tutor({
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'skills': skill,
            'experience_level': level,
            'available_days': day,
            'available_times': time
        })

    def try_create_tutor(self, data):
        try:
            self.create_tutor(data)
        except Exception as e:
            print(f"Failed to create tutor: {e}")

    def create_tutor(self, data):
        Tutor.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=self.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            skills=data['skills'],
            experience_level=data['experience_level'],
            available_days=data['available_days'],
            available_times=data['available_times']
        )

    # BOOKINGS
    def create_bookings(self):
        booking_count = Booking_requests.objects.count()
        while booking_count < self.BOOKING_COUNT:
            print(f"Seeding booking {booking_count}/{self.BOOKING_COUNT}", end='\r')
            self.generate_booking()
            booking_count = Booking_requests.objects.count()

    def generate_booking(self):
        student = random.choice(self.students)
        subject = random.choice(self.skills)[0]
        difficulty = random.choice(self.difficulty_levels)[0]
        isConfirmed = False

        self.try_create_booking({
            'student': student,
            'subject': subject,
            'difficulty': difficulty,
            'isConfirmed': isConfirmed
        })

    def try_create_booking(self, data):
        try:
            self.create_booking(data)
        except Exception as e:
            print(f"Failed to create booking: {e}")

    def create_booking(self, data):
        Booking_requests.objects.create(
            student=data['student'],
            subject=data['subject'],
            difficulty=data['difficulty'],
            isConfirmed=data['isConfirmed']
        )


# Helper functions
def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name.lower() + '.' + last_name.lower() + '@example.org'
