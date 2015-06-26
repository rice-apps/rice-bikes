from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
import re

from app.common.utils import ChoiceEnum


def validate_email(email_string):
    """
    May be unnecessary, since django appears to have built in email validation
    """
    possible_match = re.match(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', email_string)
    if possible_match is None:
        raise ValidationError('%s is not a valid email address' % email_string)


def validate_phone(phone_string):
    """
    The only validation currently necessary for a phone is that it's 10 digits
    """
    if len(phone_string) != 10:
        raise ValidationError('%s is not a valid 10-digit phone number' % phone_string)


#########################################
# Models
#########################################

class Employee(models.Model):
    user = models.OneToOneField(User)


class Transaction(models.Model):

    # CustomerForm
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, validators=[validate_email])

    service_description = models.CharField(max_length=500)
    price = models.IntegerField(default=0)

    # Auto-generated fields
    completed = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Task(models.Model):
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    transaction = models.ForeignKey(Transaction)

    def __str__(self):
        return "Task " + str(self.name)


class AllTasks():

    def __init__(self):
        self.allTasks = ['Handlebars', 'Brakes', 'Frame']

    def get_tasks(self):
        return self.allTasks
