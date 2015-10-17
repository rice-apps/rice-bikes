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
    color = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.vin)

    class Meta:
        verbose_name = "Bike Rental"
        verbose_name_plural = "Bike Rentals"


class RefurbishedBike(models.Model):
    vin = models.IntegerField(unique=True, null=False, blank=False)
    color = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)
    sold = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.vin)

    class Meta:
        verbose_name = "Bike Refurbished"
        verbose_name_plural = "Bike Refurbished"


class BuyBackBike(models.Model):
    vin = models.IntegerField(unique=True, null=False, blank=False)
    completed = models.BooleanField(default=False)
    color = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)
    price = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return str(self.vin)

    class Meta:
        verbose_name = "Bike Buy Back"
        verbose_name_plural = "Bike Buy Backs"


class Transaction(models.Model):

    # CustomerForm
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    AFFILIATION_CHOICES = (
        ('0', "Undergraduate"),
        ('1', "Graduate"), ('2', "Faculty"),
        ('3', "Staff"), ('4', "Non-Affiliate"),
        ('5', "Employee")
    )
    affiliation = models.CharField(max_length=100, choices=AFFILIATION_CHOICES, default="")
    email = models.CharField(max_length=100, validators=[validate_email])

    bike_description = models.CharField(max_length=500, null=True, blank=True)
    cost = models.IntegerField(default=0)
    amount_paid = models.IntegerField(default=0)

    # ForeignKeys to RentalBike and RefurbishedBike
    rental_bike = models.ForeignKey(RentalBike, null=True, blank=True)
    refurbished_bike = models.ForeignKey(RefurbishedBike, null=True, blank=True)
    buy_back_bike = models.ForeignKey(BuyBackBike, null=True, blank=True)

    # Auto-generated fields
    completed = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(default=datetime.now, blank=True)

    is_for_bike = models.BooleanField(default=False)

    def __str__(self):
        if not self.is_for_bike:
            return self.first_name + " " + self.last_name
        else:
            if self.rental_bike:
                return "Rental: " + self.rental_bike.color + " " + self.rental_bike.model
            elif self.refurbished_bike:
                return "Refurbished: " + self.refurbished_bike.color + " " + self.refurbished_bike.model
            else:
                return "Buy Back: " + self.buy_back_bike.color + " " + self.buy_back_bike.model


class TaskMenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField(default='0')

    def __str__(self):
        return str(self.category) + ": " + str(self.name)

    class Meta:
        verbose_name = "Menu Task Item"
        verbose_name_plural = "Menu Task Items"


class AccessoryMenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default='0')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Menu Accessory Item"
        verbose_name_plural = "Menu Accessory Items"


class PartMenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return str(self.category) + ": " + str(self.name)

    class Meta:
        verbose_name = "Menu Part Item"
        verbose_name_plural = "Menu Part Items"


class Task(models.Model):
    completed = models.BooleanField(default=False)
    number = models.IntegerField(null=False, blank=False)
    transaction = models.ForeignKey(Transaction)
    menu_item = models.ForeignKey(TaskMenuItem)
    sold = models.BooleanField(default=False)
    price = models.IntegerField(default='0')
    is_front = models.NullBooleanField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + ", " + str(self.menu_item.name)


class Accessory(models.Model):
    completed = models.BooleanField(default=False)
    number = models.IntegerField(null=False, blank=False)
    transaction = models.ForeignKey(Transaction)
    menu_item = models.ForeignKey(AccessoryMenuItem)
    sold = models.BooleanField(default=False)
    price = models.IntegerField(default='0')

    def __str__(self):
        return str(self.id) + ", " + str(self.menu_item.name)


class Part(models.Model):
    completed = models.BooleanField(default=False)
    number = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(default='0')
    transaction = models.ForeignKey(Transaction)
    menu_item = models.ForeignKey(PartMenuItem)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ", " + str(self.menu_item.name)





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

    class Meta:
        verbose_name = "Total Revenue"
        verbose_name_plural = "Total Revenue"


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
