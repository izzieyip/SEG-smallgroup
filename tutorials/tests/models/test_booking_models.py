from django.test import TestCase
from tutorials.models import Booking_requests, Confirmed_booking, Student, Tutor
from datetime import date, time

class BookingRequestsTestCase(TestCase):
    def setUp(self):
        # Create a sample student
        self.student = Student.objects.create(full_name="John Doe", email="johndoe@example.com")

        # Create booking requests
        self.booking1 = Booking_requests.objects.create(
            student=self.student,
            subject="MAT",  # Assuming "MAT" is a valid choice in Skills
            confirmed=False
        )

        self.booking2 = Booking_requests.objects.create(
            student=self.student,
            subject="SCI",  # Another valid choice in Skills
            confirmed=True
        )

    def test_booking_creation(self):
        # Test that booking requests are created correctly
        self.assertEqual(Booking_requests.objects.count(), 2)
        self.assertEqual(self.booking1.student.full_name, "John Doe")
        self.assertEqual(self.booking1.subject, "CPP")
        self.assertFalse(self.booking1.confirmed)

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
        expected_str = f"Booking Pending for: {self.student} on None at None, wants to learn {self.booking1.subject}."
        self.assertEqual(str(self.booking1), expected_str)


class ConfirmedBookingTestCase(TestCase):
    def setUp(self):
        # Create a sample student and tutor
        self.student = Student.objects.create(full_name="John Doe", email="johndoe@example.com")
        self.tutor = Tutor.objects.create(full_name="Jane Smith", email="janesmith@example.com")

        # Create a pending booking request
        self.booking_request = Booking_requests.objects.create(
            student=self.student,
            subject="CPP",
            confirmed=False
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
        self.assertEqual(self.confirmed_booking.tutor.full_name, "Jane Smith")
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
