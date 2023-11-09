import re
from django.core.mail import EmailMessage
import threading
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from django.core.mail import EmailMessage

email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
phone_regex = re.compile(r"^(\+\d{1,3})?,?\s?\d{8,13}")
username_regex = re.compile(r'^[a-zA-Z0-9_]{4,16}$')

def check_email_or_phone(user_input):
    if re.fullmatch(email_regex, user_input):
        input_type = "email"
    elif re.fullmatch(phone_regex, user_input):
        input_type = "phone"
        
    else:
        data = {
            'status':False,
            'message':'Email yoki telefon raqam hato'
        }
        raise ValidationError(data)
    return input_type

def check_user_type(user_input):
    if re.fullmatch(email_regex, user_input):
        user_input = "email"
    elif re.fullmatch(phone_regex, user_input):
        user_input = "phone"
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"
    else:
        data = {
            'status':False,
            'message':'Email, username yoki telefon raqam kiriting'
        }
        raise ValidationError(data)
    return user_input
class EmailThread(threading.Thread):
    
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send()

class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == "html":
            email.content_subtype = 'html'
        EmailThread(email).start()
    
def send_email(email, code):
    html_content = render_to_string(
        'email/code.html',
        {'code':code}
    )
    Email.send_email(
        {
            "subject": "Ruyhatdan utish uchun",
            "to_email":email,
            "body":html_content,
            "content_type":"html"
        }
    )

def send_phone(phone, code):
    print(code)

    print(f'Telefon: {phone} \n\n  {code}  ' )