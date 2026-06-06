from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .models import Hearing
import logging
from datetime import timedelta
import pytz

logger = logging.getLogger(__name__)

class HearingReminderService:
    """Service to send email reminders for hearings (2 hours before only)"""
    
    @staticmethod
    def send_reminder(hearing):
        """Send 2-hour email reminder for a hearing"""
        
        recipients = []
        
        if hearing.case.assigned_to and hearing.case.assigned_to.email:
            recipients.append(hearing.case.assigned_to.email)
        
        if hearing.case.created_by and hearing.case.created_by.email:
            recipients.append(hearing.case.created_by.email)
        
        if hearing.created_by and hearing.created_by.email:
            recipients.append(hearing.created_by.email)
        
        if not recipients:
            logger.warning(f"No recipients for hearing {hearing.id}")
            return False
        
        # Convert UTC to IST for display
        ist = pytz.timezone('Asia/Kolkata')
        local_time = hearing.hearing_date.astimezone(ist)
        date_time_str = local_time.strftime('%B %d, %Y at %I:%M %p')
        
        subject = f"⚠️ IN 2 HOURS: Hearing in {hearing.case.case_number}"
        
        message = f"""
        Dear Legal Professional,

        This is a reminder regarding an upcoming hearing in 2 hours.

        Case: {hearing.case.title} ({hearing.case.case_number})
        Hearing: {hearing.title}
        Date & Time: {date_time_str}
        Court: {hearing.court}
        Judge: {hearing.judge or 'Not specified'}

        Please ensure you are prepared.

        Thank you,
        Legal Case Management System
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=False,
            )
            
            hearing.reminder_2h_sent = True
            hearing.save()
            
            print(f"✅ 2-hour reminder sent for hearing {hearing.id}")
            logger.info(f"2-hour reminder sent for hearing {hearing.id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            logger.error(f"Failed to send email: {e}")
            return False
    
    @staticmethod
    def send_pending_reminders():
        """Check all hearings and send pending 2-hour reminders"""
        
        now = timezone.now()
        
        print("🔍 Checking for hearings that need 2-hour reminders...")
        
        hearings_2h = Hearing.objects.filter(
            hearing_date__range=[
                now + timedelta(hours=1, minutes=50),
                now + timedelta(hours=2, minutes=10)
            ],
            reminder_2h_sent=False,
            status='scheduled'
        )
        
        sent_count = 0
        for hearing in hearings_2h:
            success = HearingReminderService.send_reminder(hearing)
            if success:
                sent_count += 1
        
        print(f"✅ Reminder check completed. Sent {sent_count} reminders.")