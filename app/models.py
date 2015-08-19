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
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.vin)

class RefurbishedBike(models.Model):
    vin = models.IntegerField(unique=True, null=False, blank=False)
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.vin)


class Transaction(models.Model):

    # CustomerForm
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    AFFILIATION_CHOICES = (
        ('0', "Undergraduate"),
        ('1', "Graduate"), ('2', "Faculty"),
        ('3', "Staff"), ('4', "Non-Affiliate"),
        ('5', "Employee")
    )
    affiliation = models.CharField(max_length=100, choices=AFFILIATION_CHOICES, default="")
    email = models.CharField(max_length=100, validators=[validate_email])

    service_description = models.CharField(max_length=500, null=True, blank=True)
    cost = models.IntegerField(default=0)
    amount_paid = models.IntegerField(default=0)

    # ForeignKeys to RentalBike and RefurbishedBike
    rental_bike = models.ForeignKey(RentalBike, null=True, blank=True)
    refurbished_bike = models.ForeignKey(RefurbishedBike, null=True, blank=True)

    # Auto-generated fields
    completed = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField(default='0')

    def __str__(self):
        return str(self.category) + ": " + str(self.name)


class Task(models.Model):
    completed = models.BooleanField(default=False)
    transaction = models.ForeignKey(Transaction)
    menu_item = models.ForeignKey(MenuItem)

    def __str__(self):
        return "Task " + str(self.id) + ", " + str(self.menu_item.name)


CATEGORY_CHOICES = (
    ('0', 'Headset'),
    ('1', 'Bottom bracket'),
    ('2', 'Frame and alignment'),
    ('3', 'Brakes'),
    ('4', 'Handlebars'),
    ('5', 'Stem'),
    ('6', 'Wheels'),
    ('7', 'Shifters and derailleurs'),
    ('8', 'Saddle and seatpost'),
    ('9', 'Drive train'),
)


class PartOrder(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)
    was_ordered = models.BooleanField(default=False)
    price = models.IntegerField(default='0', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    # Auto-generated fields
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.name)


class MiscRevenueUpdate(models.Model):
    description = models.TextField()


class RevenueUpdate(models.Model):
    amount = models.IntegerField()
    employee = models.CharField(max_length=100, blank=True)
    transaction = models.ForeignKey(Transaction, blank=True, null=True)
    order = models.ForeignKey(PartOrder, blank=True, null=True)
    misc_revenue_update = models.ForeignKey(MiscRevenueUpdate, blank=True, null=True)
    new_total_revenue = models.IntegerField(blank=True)

    #Auto-generated fields
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return "Total: $" + str(self.new_total_revenue)


class TotalRevenue(models.Model):
    total_revenue = models.IntegerField()


class PartCategory(models.Model):
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)
    price = models.IntegerField(default='0', blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    was_used = models.BooleanField(default=False)
    transaction = models.ForeignKey(Transaction, blank=True)

    # Auto-generated fields
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(CATEGORY_CHOICES[int(self.category)][1]) + " for " + str(self.transaction.first_name + " "
                                                                         + self.transaction.last_name + ", ID "
                                                                         + str(self.transaction.id))