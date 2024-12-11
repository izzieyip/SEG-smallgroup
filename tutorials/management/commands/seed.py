
from tutorials.models import User, Student, Tutor, Booking_requests, Confirmed_booking, Invoices
from django.core.management.base import BaseCommand, CommandError
from django.db.models.signals import post_save
from django.dispatch import receiver

import pytz
from faker import Faker
import random
import datetime

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]

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


    days = [
    ("SUN", 'Sunday'),
    ("MON", 'Monday'),
    ("TUE", 'Tuesday'),
    ("WED", 'Wednesday'),
    ("THU", 'Thursday'),
    ("FRI", 'Friday'),
    ("SAT", 'Saturday')
    ]

    times = [
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
        self.create_fakedata()
        self.users = User.objects.all()
        self.students = Student.objects.all()
        self.tutors = Tutor.objects.all()
        print("Database seeded successfully!")


    def create_fakedata(self):
        self.generate_user_fixtures()
        self.generate_random_users()
        self.generate_bookingrequests()
        self.generate_bookings()

        
    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)
       
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
        #no other student attributes

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

        #tutor attributes
        skill = self.skills[random.randint(0,3)][0]
        level = self.difficulty_levels[random.randint(0,4)][0]
        day = self.days[random.randint(0,6)][0]
        time = self.times[random.randint(0,6)][0]


        self.try_create_tutor({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'skills': skill, 'experience_level': level, 'available_days': day, 'available_times': time})

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


    # Admin User
    def generate_admin(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        # all admin attributes same as other users

        self.try_create_admin(
            {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})

    def try_create_admin(self, data):
        try:
            self.create_admin(data)
        except Exception as e:
            print(f"Failed to create admin: {e}")

    def create_admin(self, data):
        Admin.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=self.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name']
        )

# Invoices

# added signals.py to generate random invoices when a signal that a confirmed booking
    # ... has been made is received


####################################################################################################
####################################################################################################
############   SEEDING FOR BOOKINGS AND BOOKING REQUESTS ##########################################
#####################################################################################################
####################################################################################################

    def generate_bookingrequests(self):
        requestcount = Booking_requests.objects.count()
        while requestcount < self.USER_COUNT:
            print(f"Seeding student {requestcount}/{self.USER_COUNT}", end='\r')
            self.generate_requests()
            requestcount = Booking_requests.objects.count()

        #generate confirmed bookings
        bookingcount = Confirmed_booking.objects.count()
        while bookingcount < 100:
            print(f"Seeding tutor {bookingcount}/100", end='\r')
            self.generate_bookings()
            bookingcount = Confirmed_booking.objects.count()

        print("Booking seeding complete.      ")


    #BOOKING REQUESTS
    def generate_requests(self):
        student = random.choice(Student.objects.all())
        subject = self.skills[random.randint(0,3)][0]
        level = self.difficulty_levels[random.randint(0,4)][0]

        self.try_create_bookingrequests({'student': student, 'subject': subject, 'difficulty': level})
       
    def try_create_bookingrequests(self, data):
        try:
            self.create_bookingrequests(data)
        except:
            print("failed")
            pass

    def create_bookingrequests(self, data):
        Booking_requests.objects.create(
            student=data['student'],
            subject=data['subject'],
            difficulty=data['difficulty'],
            isConfirmed=False
        )

    #CONFIRMED BOOKINGS
    def generate_bookings(self):
        booking=random.choice(Booking_requests.objects.filter(isConfirmed=False))
        tutor=random.choice(Tutor.objects.all())
        date=self.faker.date_this_year()
        time=self.faker.time('%H:%M')
        self.try_create_booking({'booking': booking, 'tutor': tutor, 'booking_date': date, 'booking_time': time})

    def try_create_booking(self, data):
        try:
            self.create_booking(data)
        except:
            print("failed")
            pass

    def create_booking(self, data):
        Confirmed_booking.objects.create(
            booking=data['booking'],
            tutor=data['tutor'],
            booking_date=data['booking_date'],
            booking_time=data['booking_time']
        )

        # when a confirmed booking is created, automatically create an invoice
        # a signal is sent to the receiver in signals.py

# Helper functions
def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name.lower() + '.' + last_name.lower() + '@example.org'
