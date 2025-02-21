from twilio.rest import Client
import streamlit as st
import os
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.twilio_client = None
        self.setup_complete = False
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
            
            if account_sid and auth_token and self.from_number:
                self.twilio_client = Client(account_sid, auth_token)
                self.setup_complete = True
        except Exception as e:
            st.warning("Notification service not configured. Some features may be limited.")
    
    def send_sms(self, to_number, message):
        """Send SMS notification using Twilio"""
        if not self.setup_complete:
            st.warning("SMS notifications are not configured.")
            return False
            
        try:
            message = self.twilio_client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return True
        except Exception as e:
            st.error(f"Failed to send SMS: {str(e)}")
            return False
    
    def schedule_reminder(self, patient_data, reminder_type, schedule):
        """Schedule a reminder for medication or appointment"""
        if not patient_data.get('personal_info', {}).get('phone'):
            st.warning("Please update your phone number to receive reminders.")
            return
            
        message = self._generate_reminder_message(patient_data, reminder_type, schedule)
        return self.send_sms(patient_data['personal_info']['phone'], message)
    
    def _generate_reminder_message(self, patient_data, reminder_type, schedule):
        """Generate appropriate reminder message"""
        name = patient_data['personal_info'].get('name', 'Patient')
        
        if reminder_type == 'medication':
            return (f"Hello {name}, this is a reminder to take your "
                   f"medication according to schedule: {schedule}")
        elif reminder_type == 'appointment':
            return (f"Hello {name}, you have an upcoming medical "
                   f"appointment scheduled for: {schedule}")
        else:
            return (f"Hello {name}, this is a reminder for your "
                   f"healthcare activity: {schedule}")

# Initialize notification service
notification_service = NotificationService()

def send_notification(to_number, message):
    """Wrapper function for sending notifications"""
    return notification_service.send_sms(to_number, message)
