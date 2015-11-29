from app.models import Transaction, RentalBike, RefurbishedBike, RevenueUpdate, \
    MiscRevenueUpdate, BuyBackBike, PartMenuItem
from django import forms
from django.forms import Form, ModelForm
from django.contrib.auth.models import User


class RepairsForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ("bike_description", "cost",)


class CustomerForm(ModelForm):
    rental_vin = forms.IntegerField(required=False)
    refurbished_vin = forms.IntegerField(required=False)
    buy_back_vin = forms.IntegerField(required=False)

    class Meta:
        model = Transaction
        fields = ("first_name", "last_name", "email", "affiliation", "bike_description")

    def save(self, commit=True):
        # do something with self.cleaned_data['rental_vin']
        return super(CustomerForm, self).save(commit=commit)

    def clean(self):
        return self.cleaned_data


class TaskForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('bike_description', 'cost', 'amount_paid', 'email')


class RentalForm(ModelForm):
    class Meta:
        model = RentalBike
        fields = ('vin', 'color', 'model')


class RefurbishedForm(ModelForm):
    class Meta:
        model = RefurbishedBike
        fields = ('vin', 'color', 'model')


class BuyBackForm(ModelForm):
    class Meta:
        model = BuyBackBike
        fields = ('vin', 'color', 'model')


class RevenueForm(ModelForm):
    class Meta:
        model = RevenueUpdate


class PartOrderForm(Form):
    part = forms.ModelChoiceField(queryset=PartMenuItem.objects.all())
    number = forms.IntegerField()
    description = forms.CharField(required=False)


class MiscRevenueUpdateForm(ModelForm):
    class Meta:
        model = MiscRevenueUpdate


class SingleNumberForm(Form):
    number = forms.IntegerField(label='Number', initial=1)

class SinglePriceForm(Form):
    price = forms.IntegerField(label='Price', initial=0)

