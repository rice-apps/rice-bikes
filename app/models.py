from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

#########################################
# Validation methods
#########################################


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


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    affiliation = models.CharField(max_length=100, default="")
    # phone = models.CharField(default="", max_length=100, validators=[validate_phone])
    completed = models.BooleanField(default=False)  # This should represent a customer having picked up his or her bike
    date_submitted = models.DateTimeField('date submitted')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Service(models.Model):
    type = models.CharField(max_length=500, default="None")
    price = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer)
    fulfilled = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, default=None)    # Represents the employee who performed this service


class Part(models.Model):
    type = models.CharField(max_length=500)
    price = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer)
    fulfilled = models.BooleanField(default=False)
    # employee = models.ForeignKey(Employee)