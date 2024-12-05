"""Unit tests of the request booking form."""
from django import forms
from django.test import TestCase
from tutorials.forms import CreateBookingRequest
from tutorials.models import Student, Booking_requests

#THIS TESTS ARE NOT WORKING !!! DO NOT COMMIT !!!
class BookingRequestTestCase(TestCase):
    """Unit tests of the request booking form."""
    def setUp(self):
        self.student = Student.objects.create(first_name ='Jane',
            last_name = 'Doe',
            username ='@janedoe',
            email ='janedoe@example.org',)
        
        self.student.set_password("Password123")
        self.student.save()
        self.assertTrue(self.student)
        
        self.form_input = {
            "student" :self.student,
            "subject" : "DJ",
            "difficulty" : "5"
        }

    def test_valid_booking_request_form(self):
        form = CreateBookingRequest(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_booking_request_form_has_necessary_fields(self):
        form = CreateBookingRequest()
        self.assertIn('student', form.fields)
        self.assertIn("subject", form.fields)
        self.assertIn("difficulty", form.fields)

    def test_booking_request_form_must_save_correctly(self):
        form = CreateBookingRequest(data = self.form_input)
        before_count = Booking_requests.objects.count()
        form.save()
        after_count = Booking_requests.objects.count()
        self.assertEqual(after_count, before_count+1)
        thisForm = Booking_requests.objects.get(id = form.id)
        #self.assertEqual(thisForm.student, self.student)
        self.assertEqual(thisForm.subject, 'DJ')   
        self.assertEqual(thisForm.difficulty, "5") 

    