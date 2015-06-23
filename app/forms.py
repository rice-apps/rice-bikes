from app.models import Transaction
from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User


class CustomerForm(Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    affiliation = forms.CharField(max_length=100)
    no_receipt = forms.BooleanField(required=False)


class TasksForm(Form):
    handlebars = forms.BooleanField(required=False)
    brakes = forms.BooleanField(required=False)
    frame = forms.BooleanField(required=False)

    @staticmethod
    def get_info_dict():
        info_dict = {
            'Handlebars': {'price': 55, 'category': 'Hard'},
            'Brakes': {'price': 3, 'category': 'Hard'},
            'Frame': {'price': 2, 'category': 'Easy'}
        }
        return info_dict


class RepairsForm(TasksForm):
    service_description = forms.CharField(max_length=100)
    price = forms.CharField(max_length=10)


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



