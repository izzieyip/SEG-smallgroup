# these tests were written by AI
from django.test import TestCase
from django.urls import reverse
from tutorials.models import Booking_requests, Tutor, User, Student
from tutorials.forms import ConfirmedBookingForm

class DisplayAllBookingRequestsTest(TestCase):

    def setUp(self):
        # Create some users, tutors, and booking requests
        self.user = User.objects.create_user(username='@admin', first_name='Admin', last_name='User', email='admin@example.com', password='password')
        self.student_user = Student.objects.create_user(username='@student', first_name='Student', last_name='User', email='student@example.com', password='password')
        self.tutor_user = Tutor.objects.create_user(username='@tutor', first_name='Tutor', last_name='User', email='tutor@example.com', password='password', skills='PY', experience_level=3, available_days='MON', available_times=1)
        self.booking_request = Booking_requests.objects.create(student= self.student_user, subject='PY', isConfirmed=False)
        self.url = reverse('view_requests')  

    def test_display_all_unconfirmed_booking_requests(self):
        # Login as an admin
        self.client.login(username='@admin', password='password')

        # Send request and check response
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_requests.html')

        # Check if booking requests are in the context
        self.assertIn('data', response.context)
        self.assertEqual(len(response.context['data']), 1)  # Should have one unconfirmed booking request
        self.assertContains(response, self.booking_request.subject)

