from django.db import models
from django.core.exceptions import ValidationError
import re


def validate_email(email_string):
    possible_match = re.match(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', email_string)
    if possible_match is None:
        raise ValidationError(u'%s is not a valid email address' % email_string)


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, validators=[validate_email])
    service_description = models.CharField(max_length=500)
    price = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_submitted = models.DateTimeField('date submitted')

    def __str__(self):
        return self.first_name + " " + self.last_name