"""
django signal is a way to enable a communication between differnt parts of a program
we might wanna use signal to notify some part about some event that has occured.
foreg: when user is create we wanna send them a email, user creation is a event and sending email is a function
the part of program that sends signal is receiver and other is sender.

Types of signals
1.Model Signals: Sent by models when a instance is created.
2. Request/Res signal: sent during request/res cycle.

we can define the receiver using decorator
"""

from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Income

@receiver(post_save, sender=Income)
def greet_user(sender, instance, created, **kwargs):
    print("greeting user")
    if created:
        try:
            send_mail(
                subject="Welcome",
                message="Welcome to our site!",
                from_email=["bishwasxdgautam@gmail.com"],
                recipient_list=["gautambishwas7@gmail.com"],
                fail_silently=False,
            )
            print(f"Welcome email sent successfully to ")
        except Exception as e:
            print(f"Error sending email to : {repr(e)}")
