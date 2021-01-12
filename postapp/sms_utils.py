from django.conf import settings
import africastalking

"""

AFRICA'S TALKING SETUP

"""

username = 'Kizaagri'
api_key = 'f798724424c4bbb1eb38f3a954546d2dc37e6b28cde86e2071510335c3883838'

africastalking.initialize(username, api_key)
sms_backend = africastalking.SMS


def send_sms(phone_numbers, message):
    sms_backend.send(message=message, recipients=phone_numbers)
