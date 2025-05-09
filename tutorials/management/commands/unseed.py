from django.core.management.base import BaseCommand, CommandError
from tutorials.models import User

class Command(BaseCommand):
    """Build automation command to unseed the database."""
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        """Unseed the database."""

        User.objects.filter(is_staff=False).delete()
        Booking_requests.objects.all().delete()
        Confirmed_booking.objects.all().delete()
        Invoices.objects.all().delete()
