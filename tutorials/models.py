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

#placeholders to avoid error
class Student(User):
    pass

#placeholders to avoid error
class Tutor(User):
    pass





#Pending Bookings class (no tutor assigned)
#Refers to objects of the student class
#Student is a foreign key to student ID
#can access the data using "student = Student.objects.get(id="THE ID NUMBER")"
class Pending_booking(models.Model):
    #on_delete=models.CASCADE ensure if a student is removed from the students model, their pending bookings are deleted too
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="pending_bookings")
    booking_date = models.DateField()
    booking_time = models.TimeField()

    def __str__(self):
        return f"Booking Pending for: {self.student} on {self.booking_date} at {self.booking_time}"

    #ensures each one is unique
    class Meta:
        unique_together = ('student', 'booking_date', 'booking_time')

#Confirmed Bookings class (tutor assigned)
#Refers to objects of the tutor and Pending_booking classes
#Tutor is a foreign key to tutor ID
#booking is a foreign key to Pending_booking ID
#can access the data using "booking = Pending_booking.objects.get(id="THE ID NUMBER")"
class Confirmed_booking(models.Model):
    #on_delete=models.CASCADE ensure if a student is removed from the students model, their pending bookings are deleted too
    booking = models.ForeignKey(Pending_booking, on_delete=models.CASCADE, related_name="confirmed_booking")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="confirmed_bookings")

    def __str__(self):
        return f"Booking: {self.booking.student} with {self.tutor} on {self.booking.booking_date} at {self.booking.booking_time}"

    #ensures each one is unique
    class Meta:
        unique_together = ('booking', 'tutor')
