from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Confirmed_booking, Invoices
import random
import datetime

@receiver(post_save, sender=Confirmed_booking)
def create_invoice_on_booking(sender, instance, created, **kwargs):
    # this method gets called when a confirmed booking is created

    # choosing random values for the fields in invoices
    if created:
        # uses the student linked to the booking request
        student = instance.booking.student

        # generates random amounts for other fields
        amount = random.randint(100, 400)
        year = random.randint(2024, 2025)
        paid = random.choice([True, False])

        Invoices.objects.create(
            # link the invoice to the confirmed_booking
            booking=instance,
            # link the invoice to the student as well
            student=student,
            amount=amount,
            year=year,
            paid=paid
        )

        # this is for debugging
        print(f"Invoice created for {student.username} with amount: {amount}")

    else:
        print(f"Invoice creation failed")