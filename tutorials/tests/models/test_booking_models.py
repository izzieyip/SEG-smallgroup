
from django.test import TestCase
from tutorials.models import Booking_requests, Confirmed_booking, Student, Tutor
from datetime import date, time

class BookingRequestsTestCase(TestCase):
    def setUp(self):
        # Create a sample student
        self.student = Student.objects.create(first_name="John", last_name="Doe", username="@johndoe", email="johndoe@example.com")

        # Create booking requests
        self.booking1 = Booking_requests.objects.create(
            student=self.student,
            subject="CPP",
            isConfirmed=False,
            difficulty=1,
        )

        self.booking2 = Booking_requests.objects.create(
            student=self.student,
            subject="JAVA",  # Another valid choice in Skills
            isConfirmed=True,
            difficulty=2,
        )

    def test_booking_creation(self):
        # Test that booking requests are created correctly
        self.assertEqual(Booking_requests.objects.count(), 2)
        self.assertEqual(self.booking1.student.first_name, "John")
        self.assertEqual(self.booking1.subject, "CPP")
        self.assertFalse(self.booking1.isConfirmed)

    def test_unique_together_constraint(self):
        # Test that duplicate (student, subject) combinations are not allowed
        with self.assertRaises(Exception):
            Booking_requests.objects.create(
                student=self.student,
                subject="CPP",
                confirmed=False
            )

    def test_str_method(self):
        # Test the string representation of a booking request
        expected_str = f"Booking Pending for: {self.student} wants to learn {self.booking1.subject} at difficulty level {self.booking1.difficulty}."
        self.assertEqual(str(self.booking1), expected_str)


class ConfirmedBookingTestCase(TestCase):
    def setUp(self):
        # Create a sample student and tutor
        self.student = Student.objects.create(first_name="John", last_name="Doe", username="@johndoe", email="johndoe@example.com")
        self.tutor = Tutor.objects.create(first_name="Jane", last_name="Smith", username="@janesmith", email="janesmith@example.com", experience_level=1, skills="CPP")

        # Create a pending booking request
        self.booking_request = Booking_requests.objects.create(
            student=self.student,
            subject="CPP",
            isConfirmed=False,
            difficulty = 4
        )

        # Create a confirmed booking
        self.confirmed_booking = Confirmed_booking.objects.create(
            booking=self.booking_request,
            tutor=self.tutor,
            booking_date=date(2024, 11, 18),
            booking_time=time(14, 30)
        )

    def test_confirmed_booking_creation(self):
        # Test that the confirmed booking is created correctly
        self.assertEqual(Confirmed_booking.objects.count(), 1)
        self.assertEqual(self.confirmed_booking.booking, self.booking_request)
        self.assertEqual(self.confirmed_booking.tutor.first_name, "Jane")
        self.assertEqual(self.confirmed_booking.booking_date, date(2024, 11, 18))
        self.assertEqual(self.confirmed_booking.booking_time, time(14, 30))

    def test_unique_together_constraint(self):
        # Test that duplicate (booking, tutor, booking_date, booking_time) combinations are not allowed
        with self.assertRaises(Exception):
            Confirmed_booking.objects.create(
                booking=self.booking_request,
                tutor=self.tutor,
                booking_date=date(2024, 11, 18),
                booking_time=time(14, 30)
            )

    def test_str_method(self):
        # Test the string representation of a confirmed booking
        expected_str = f"Booking: {self.student.full_name} with {self.tutor.full_name} on 2024-11-18 at 14:30:00, learning {self.booking_request.subject}."
        self.assertEqual(str(self.confirmed_booking), expected_str)
