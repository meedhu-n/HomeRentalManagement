from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Property

class Command(BaseCommand):
    help = 'Check and hide properties with expired plans'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        # Find properties with expired plans that are still visible
        expired_properties = Property.objects.filter(
            plan_expiry_date__lte=now,
            status=Property.Status.AVAILABLE
        )
        
        count = expired_properties.count()
        
        if count > 0:
            # Change status to PENDING_APPROVAL or MAINTENANCE
            expired_properties.update(status=Property.Status.PENDING_APPROVAL)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully hidden {count} expired properties'
                )
            )
            
            # List the properties
            for prop in expired_properties:
                self.stdout.write(
                    f'  - {prop.title} (Owner: {prop.owner.username}, Plan: {prop.plan_type}, Expired: {prop.plan_expiry_date})'
                )
        else:
            self.stdout.write(
                self.style.SUCCESS('No expired properties found')
            )
