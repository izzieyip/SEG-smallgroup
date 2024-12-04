from django.core.exceptions import ValidationError
from django.test import TestCase
from tutorials.models import Invoices, Student
import datetime

class BookingRequestsTestCase(TestCase):
    def setUp(self):
        # Create a sample student
        self.student = Student.objects.create(first_name="John", last_name = "Doe", username="@johndoe", email="johndoe@example.com")
        self.invoice = Invoices.objects.create(student=self.student, year = 2020, amount = 100, paid = False)

    def test_create_invoice(self):
        year = datetime.date.today().year
        invoice2 = Invoices.objects.create(student=self.student, year = year, amount = 100, paid = False)

    def test_invoice_str_method(self):
        # checking if the __str__ method works
        expected_str = f"{self.student.first_name} has an invoice of amount: {self.invoice.amount}. Invoice created in : {self.invoice.year}"
        self.assertEqual(str(self.invoice), expected_str)

    def test_student_blank(self):
        # testing when attributes are left blank
        self.invoice.student = None
        self._assert_invoice_is_invalid()
    
    def test_year_blank(self):
        self.invoice.year = ""
        self._assert_invoice_is_invalid()

    def test_amount_blank(self):
        self.invoice.amount = ""
        self._assert_invoice_is_invalid()

    def test_paid_blank(self):
        self.invoice.paid = None
        self._assert_invoice_is_invalid()

    def _assert_invoice_is_valid(self):
        try:
            self.invoice.full_clean()
        except (ValidationError):
            self.fail('Test INVOICE should be valid')

    def _assert_invoice_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invoice.full_clean()
    



    


