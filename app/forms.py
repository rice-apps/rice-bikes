from django.forms import ModelForm
from app.models import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'service_description','completed', 'date_submitted']