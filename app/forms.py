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


class RepairsForm(ModelForm):

    handlebars = forms.BooleanField(required=False)
    brakes = forms.BooleanField(required=False)
    frame = forms.BooleanField(required=False)

    class Meta:
        model = Transaction
        fields = ['handlebars', 'brakes', 'frame']


class RepairsFormSubmit(Form):
    handlebars = forms.BooleanField(required=False)
    brakes = forms.BooleanField(required=False)
    frame = forms.BooleanField(required=False)
    service_description = forms.CharField(max_length=100)
    price = forms.CharField(max_length=10)


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



