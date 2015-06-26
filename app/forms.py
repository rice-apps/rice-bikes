from app.models import Transaction
from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User

FRAME_AND_ALIGNMENT_CHOICES = [("derailleur", "Align Derailleur Hanger"), ("clean", "Basic Clean"),
                               ("basket", "Install Front Basket")]
HANDLEBARS_CHOICES = [("grips", "Install Grips"), ("handlebars", "Install Handlebars")]
BRAKES_CHOICES = [("rim-brake", "Adjust Rim Brake"), ("disk-brake", "Adjust Disc Brake")]

class CustomerForm(Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    affiliation = forms.CharField(max_length=100)
    no_receipt = forms.BooleanField(required=False)


class TasksForm(Form):
    Handlebars = forms.BooleanField(required=False)
    Brakes = forms.BooleanField(required=False)
    Frame = forms.BooleanField(required=False)

    @staticmethod
    def get_info_dict():
        info_dict = {
            'Handlebars': {'price': 55, 'category': 'Hard'},
            'Brakes': {'price': 3, 'category': 'Hard'},
            'Frame': {'price': 2, 'category': 'Easy'}
        }
        return info_dict

    @staticmethod
    def get_category_dict():
        info_dict_hard = {
            'Handlebars': {'price': 55},
            'Brakes': {'price': 3}
        }
        info_dict_easy = {
            'Frame': {'price': 2}
        }
        category_dict = {
            'Hard': info_dict_hard,
            'Easy': info_dict_easy
        }
        return category_dict

    @staticmethod
    def get_non_task_fields():
        return ('Service description',
                'Price')


class RepairsForm(TasksForm):
    service_description = forms.CharField(max_length=100)
    price = forms.CharField(max_length=10)


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



