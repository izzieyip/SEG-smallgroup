from django.test import TestCase
from tutorials.models import Booking_requests, Tutor, Confirmed_booking, Invoices, Student


# invoices should be created every time a confirmed booking is made
# the process should be automatic since it is done with signals

class InvoiceSignalTestCase(TestCase):
    def setUp(self):
        # Create a student, tutor and booking request to use

        self.student = Student.objects.create(
            username = "@TestStudent",
            email = "teststudent@example.com",
            first_name = "Test",
            last_name = "Student",
            password = "Password123"
        )

        self.booking_request = Booking_requests.objects.create(
            student_id = self.student,
            subject="CPP",
            difficulty = 3,
            isConfirmed=False
        )

        self.tutor = Tutor.objects.create(
            username = "@SamBob",
            first_name = "Sam",
            last_name = "Bob",
            email = "sambob@example.com",
            skills = "CPP",
            password = "Password123",
            experience_level = 3,
            available_days = "SUN",
            available_times = 1
        )

    def test_invoice_created_on_confirmed_booking(self):
        # Create a Confirmed_booking

        confirmed_booking = Confirmed_booking.objects.create(
            booking=self.booking_request,
            tutor=self.tutor,
            booking_date="2024-06-15",
            booking_time="12:00:00"
        )

        # Check if an invoice was created
        invoice = Invoices.objects.filter(booking=confirmed_booking).first()
        self.assertIsNotNone(invoice, "Invoice was not created")
        print(f"Invoice created successfully for Booking ID: {confirmed_booking.id}")
