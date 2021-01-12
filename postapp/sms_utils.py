from django.conf import settings
import africastalking

"""

AFRICA'S TALKING SETUP

"""

username = 'Kizaagri'
api_key = 'c6456d5c3c95593e818d0fc10bc5082feeb9020bb704a888fa04007223322602'

africastalking.initialize(username, api_key)
sms_backend = africastalking.SMS


def send_sms(phone_numbers, message):
    sms_backend.send(message=message, recipients=phone_numbers)
