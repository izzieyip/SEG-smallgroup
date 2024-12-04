
from django.test import TestCase
from django import forms
from tutorials.models import Booking_requests, Confirmed_booking, Student, Tutor
from tutorials.forms import BookingForm
import datetime


class BookingFormTestCase(TestCase):
    def setUp(self):
        self.tutor = Tutor.objects.create(first_name = "Peter", last_name = "Pickles", email = "peter@hotmail.com", username = "@peter", skills = "CPP", experience_level = "1", available_days = "MON", available_times = "7")
        self.student = Student.objects.create(first_name="John", last_name="Doe", username="@johndoe", email="johndoe@example.com")

        self.form_input = {
            'student' : Student.objects.get(username='@johndoe'),
            'subject' : 'CPP',
            'date' : datetime.date.today(),
            'time' : datetime.time(12,0),
            'tutor' : Tutor.objects.get(username='@peter')
        }

    def test_form_has_nec_fields(self):
        form = BookingForm()
        self.assertIn('student', form.fields)
        self.assertIn('subject', form.fields)
        self.assertIn('date', form.fields)
        date_field = form.fields['date']
        self.assertTrue(isinstance(date_field, forms.DateField))
        self.assertIn('time', form.fields)
        self.assertIn('tutor', form.fields)

    def test_form_valid(self):
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_student_invalid(self):
        self.form_input['student'] = ""
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_subject_invalid(self):
        self.form_input['subject'] = ""
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_false_subject_invalid(self):
        self.form_input['subject'] = "c#"
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_date_invalid(self):
        self.form_input['date'] = None
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_time_invalid(self):
        self.form_input['time'] = None
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_tutor_invalid(self):
        self.form_input['tutor'] = ""
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    