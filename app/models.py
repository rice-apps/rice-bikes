from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
import re


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


class RentalBike(models.Model):
    vin = models.IntegerField(unique=True, null=False, blank=False)


class RefurbishedBike(models.Model):
    vin = models.IntegerField(unique=True, null=False, blank=False)


class Transaction(models.Model):

    # CustomerForm
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, validators=[validate_email])

    service_description = models.CharField(max_length=500)
    price = models.IntegerField(default=0)

    # ForeignKeys to RentalBike and RefurbishedBike
    rental_bike = models.ForeignKey(RentalBike, null=True, blank=True)
    refurbished_bike = models.ForeignKey(RefurbishedBike, null=True, blank=True)

    # Auto-generated fields
    completed = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Task(models.Model):
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    transaction = models.ForeignKey(Transaction)

    def __str__(self):
        return "Task " + str(self.name)


class RevenueUpdate(models.Model):
    amount = models.IntegerField()
    employee = models.CharField(max_length=100)
    completed_transaction = models.ForeignKey(Transaction)
    description = models.CharField(max_length=100)
    is_transaction = models.BooleanField(default=False)


class TotalRevenue(models.Model):
    total_revenue = models.IntegerField()












