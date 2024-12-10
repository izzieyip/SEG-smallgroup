from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Confirmed_booking, Invoices
import random
import datetime

@receiver(post_save, sender=Confirmed_booking)
def create_invoice_on_booking(self, sender, instance, created, **kwargs):
    # this method gets called when a confirmed booking is created

    # choosing random values for the fields in invoices
    if created:
        student = instance.booking.student
        amount = random.randint(100, 400)
        year = random.randint(2024, 2025)
        paid = random.choice([True, False])

        Invoice.objects.create(
            student=student,
            amount=amount,
            year=year,
            paid=paid
        )

        # this is for debugging
        print(f"Invoice created for {student.username} with amount: {amount}")
