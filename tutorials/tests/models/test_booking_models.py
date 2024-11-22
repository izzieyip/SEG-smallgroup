from django.test import TestCase
from tutorials.models import Student, Tutor, Pending_booking, Confirmed_booking
from datetime import date, time

class BookingTests(TestCase):

    def setUp(self):
        # Create sample data for testing
        # TO DO: adjust to finalised tutor and student models
        self.student = Student.objects.create(name="Alice", email="alice@example.com")
        self.tutor = Tutor.objects.create(name="Mr. Smith", email="smith@example.com", subject="Math")
        self.booking_date = date(2024, 12, 1)
        self.booking_time = time(14, 0)

    def test_create_pending_booking(self):
        # Test creating a Pending_booking instance
        pending_booking = Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        self.assertIsNotNone(pending_booking.id)
        self.assertEqual(pending_booking.student, self.student)
        self.assertEqual(pending_booking.booking_date, self.booking_date)
        self.assertEqual(pending_booking.booking_time, self.booking_time)

    def test_pending_booking_str_method(self):
        # Test the __str__ method of Pending_booking
        pending_booking = Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        expected_str = f"Booking Pending for: {self.student} on {self.booking_date} at {self.booking_time}"
        self.assertEqual(str(pending_booking), expected_str)

    def test_unique_pending_booking(self):
        # Test that creating a duplicate Pending_booking raises an error
        Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        with self.assertRaises(Exception):
            Pending_booking.objects.create(
                student=self.student,
                booking_date=self.booking_date,
                booking_time=self.booking_time
            )

    def test_create_confirmed_booking(self):
        # Test creating a Confirmed_booking instance
        pending_booking = Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        confirmed_booking = Confirmed_booking.objects.create(
            booking=pending_booking,
            tutor=self.tutor
        )
        self.assertIsNotNone(confirmed_booking.id)
        self.assertEqual(confirmed_booking.booking, pending_booking)
        self.assertEqual(confirmed_booking.tutor, self.tutor)

    def test_confirmed_booking_str_method(self):
        # Test the __str__ method of Confirmed_booking
        pending_booking = Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        confirmed_booking = Confirmed_booking.objects.create(
            booking=pending_booking,
            tutor=self.tutor
        )
        expected_str = f"Booking: {self.student} with {self.tutor} on {self.booking_date} at {self.booking_time}"
        self.assertEqual(str(confirmed_booking), expected_str)

    def test_unique_confirmed_booking(self):
        # Test that creating a duplicate Confirmed_booking raises an error
        pending_booking = Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        Confirmed_booking.objects.create(
            booking=pending_booking,
            tutor=self.tutor
        )
        with self.assertRaises(Exception):
            Confirmed_booking.objects.create(
                booking=pending_booking,
                tutor=self.tutor
            )

    def test_delete_student_cascade(self):
        # Test that deleting a student deletes related Pending_booking instances
        pending_booking = Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        self.student.delete()
        with self.assertRaises(Pending_booking.DoesNotExist):
            Pending_booking.objects.get(id=pending_booking.id)

    def test_delete_pending_booking_cascade(self):
        # Test that deleting a Pending_booking deletes related Confirmed_booking instances
        pending_booking = Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        confirmed_booking = Confirmed_booking.objects.create(
            booking=pending_booking,
            tutor=self.tutor
        )
        pending_booking.delete()
        with self.assertRaises(Confirmed_booking.DoesNotExist):
            Confirmed_booking.objects.get(id=confirmed_booking.id)

    def test_delete_tutor_cascade(self):
        # Test that deleting a tutor deletes related Confirmed_booking instances
        pending_booking = Pending_booking.objects.create(
            student=self.student,
            booking_date=self.booking_date,
            booking_time=self.booking_time
        )
        confirmed_booking = Confirmed_booking.objects.create(
            booking=pending_booking,
            tutor=self.tutor
        )
        self.tutor.delete()
        with self.assertRaises(Confirmed_booking.DoesNotExist):
            Confirmed_booking.objects.get(id=confirmed_booking.id)
