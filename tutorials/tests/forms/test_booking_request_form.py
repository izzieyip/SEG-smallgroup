from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Student, Tutor, Booking_requests, Confirmed_booking

class BookingRequestsModelTest(TestCase):
    def setUp(self):
        """Set up test data for Booking_requests."""
        self.student = Student.objects.create_user(
            username='@student123',
            email='student@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.tutor = Tutor.objects.create_user(
            username='@tutor456',
            email='tutor@example.com',
            password='password123',
            first_name='Jane',
            last_name='Smith',
            skills='PY',
            experience_level=3,
            available_days='MON',
            available_times=1
        )
        self.booking_request = Booking_requests.objects.create(
            student=self.student,
            subject='PY',
            difficulty=3,
            isConfirmed=False
        )

    def test_booking_request_creation(self):
        """Test creating a booking request."""
        self.assertEqual(self.booking_request.student, self.student)
        self.assertEqual(self.booking_request.subject, 'PY')
        self.assertEqual(self.booking_request.difficulty, 3)
        self.assertFalse(self.booking_request.isConfirmed)

    def test_unique_booking_request(self):
        """Test that a unique constraint prevents duplicate bookings for the same student and subject."""
        with self.assertRaises(ValidationError):
            duplicate_booking = Booking_requests(
                student=self.student,
                subject='PY',
                difficulty=3
            )
            duplicate_booking.full_clean()  # Triggers validation

    def test_booking_request_str(self):
        """Test the string representation of Booking_requests."""
        self.assertEqual(
            str(self.booking_request),
            f"Booking Pending for: {self.student} wants to learn PY at difficulty level 3."
        )

class ConfirmedBookingModelTest(TestCase):
    def setUp(self):
        """Set up test data for Confirmed_booking."""
        self.student = Student.objects.create_user(
            username='@student123',
            email='student@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.tutor = Tutor.objects.create_user(
            username='@tutor456',
            email='tutor@example.com',
            password='password123',
            first_name='Jane',
            last_name='Smith',
            skills='PY',
            experience_level=3,
            available_days='MON',
            available_times=1
        )
        self.booking_request = Booking_requests.objects.create(
            student=self.student,
            subject='PY',
            difficulty=3,
            isConfirmed=False
        )
        self.confirmed_booking = Confirmed_booking.objects.create(
            booking=self.booking_request,
            tutor=self.tutor,
            booking_date='2024-01-01',
            booking_time='10:00:00'
        )

    def test_confirmed_booking_creation(self):
        """Test creating a confirmed booking."""
        self.assertEqual(self.confirmed_booking.booking, self.booking_request)
        self.assertEqual(self.confirmed_booking.tutor, self.tutor)
        self.assertEqual(self.confirmed_booking.booking_date, '2024-01-01')
        self.assertEqual(self.confirmed_booking.booking_time, '10:00:00')

    def test_booking_request_marked_as_confirmed(self):
        """Test that the related booking request is marked as confirmed when a confirmed booking is created."""
        self.booking_request.refresh_from_db()
        self.assertTrue(self.booking_request.isConfirmed)

    def test_unique_confirmed_booking(self):
        """Test that a unique constraint prevents duplicate confirmed bookings."""
        with self.assertRaises(ValidationError):
            duplicate_confirmed_booking = Confirmed_booking(
                booking=self.booking_request,
                tutor=self.tutor,
                booking_date='2024-01-01',
                booking_time='10:00:00'
            )
            duplicate_confirmed_booking.full_clean()  # Triggers validation

    def test_confirmed_booking_str(self):
        """Test the string representation of Confirmed_booking."""
        self.assertEqual(
            str(self.confirmed_booking),
            f"Booking: {self.booking_request.student.full_name()} with {self.tutor.full_name()} on 2024-01-01 at 10:00:00, learning {self.booking_request.subject}."
        )
