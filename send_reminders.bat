@echo off
cd C:\Users\Lenovo 1024\Desktop\legal-case-management\backend
call venv\Scripts\activate
python manage.py shell -c "from calendar_app.services import HearingReminderService; HearingReminderService.send_pending_reminders()"