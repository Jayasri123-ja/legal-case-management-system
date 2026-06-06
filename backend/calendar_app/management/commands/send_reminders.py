from django.core.management.base import BaseCommand
from calendar_app.services import HearingReminderService

class Command(BaseCommand):
    help = 'Send hearing reminders'
    
    def handle(self, *args, **options):
        self.stdout.write('Sending reminders...')
        HearingReminderService.send_pending_reminders()
        self.stdout.write('Done!')