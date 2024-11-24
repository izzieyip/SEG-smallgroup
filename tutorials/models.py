
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
import datetime

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
    
Skills = [
    ("CPP", "C++"),
    ("JA", "JAVA"),
    ("PY", "PYTHON"),
    ("DJ", "DJANGO")
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

difficulty_levels = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5")
]


class Student(User):
    skill_to_learn = models.CharField(choices = Skills, max_length= 3, default=None)
    difficulty_level = models.IntegerField(choices= difficulty_levels, default=None)

    def __str__(self) -> str:
        return super().__str__() + f'wants to learn {self.skill_to_learn} at difficulty level {self.difficulty_level}'

class Tutor(User):
    skills = models.CharField(choices = Skills, max_length= 3, default=None)
    experience_level = models.IntegerField(choices= difficulty_levels, default=None)

    def __str__(self) -> str:
        return super().__str__() + f'knows {self.skills} with an experience level of {self.experience_level}'


class Availability(models.Model):
    tutor_id = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    available_day = models.CharField(choices=days, max_length=3)
    available_time = models.IntegerField(choices=times)

    def __str__(self) -> str:
        return f'{self.tutor_id.first_name} is available at {self.available_day} for the {self.available_time}'


#Pending Bookings class (no tutor assigned)
#Refers to objects of the student class
#Student is a foreign key to student ID
#can access the data using "student = Student.objects.get(id="THE ID NUMBER")"
class Booking_requests(models.Model):
    #on_delete=models.CASCADE ensure if a student is removed from the students model, their pending bookings are deleted too
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="pending_bookings")
    subject = models.CharField(choices = Skills, max_length= 3)
    isConfirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking Pending for: {self.student} on {self.booking_date} at {self.booking_time}"

    #ensures each one is unique
    class Meta:
        unique_together = ('student', 'subject')

#Confirmed Bookings class (tutor assigned)
#Refers to objects of the tutor and Pending_booking classes
#Tutor is a foreign key to tutor ID
#booking is a foreign key to Pending_booking ID
#can access the data using "booking = Pending_booking.objects.get(id="THE ID NUMBER")"
class Confirmed_booking(models.Model):
    #on_delete=models.CASCADE ensure if a student is removed from the students model, their pending bookings are deleted too
    booking = models.ForeignKey(Booking_requests, on_delete=models.CASCADE, related_name="confirmed_booking")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="confirmed_bookings")
    booking_date = models.DateField(default=datetime.date.today)
    booking_time = models.TimeField(default=datetime.time(12, 0))
    
    #updates the booking reqeust confirmed
    def save(self, *args, **kwargs):
        # Update the confirmed field of the related booking object in the booking_request model
        self.booking.isConfirmed = True
        self.booking.save()  # Save the updated Booking_requests instance
        super().save(*args, **kwargs)  # Save the Confirmed_booking instance

    def __str__(self):
        return f"Booking: {self.booking.student.full_name} with {self.tutor.full_name} on {self.booking_date} at {self.booking_time}, learning {self.booking.subject}."

    #ensures each one is unique
    class Meta:
        unique_together = ('booking', 'tutor', 'booking_date', 'booking_time')
