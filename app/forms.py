from app.models import Transaction, RentalBike, RefurbishedBike, RevenueUpdate, PartCategory, PartOrder
from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User


class RepairsForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ("service_description", "cost",)


class CustomerForm(ModelForm):
    rental_vin = forms.IntegerField(required=False)
    refurbished_vin = forms.IntegerField(required=False)

    class Meta:
        model = Transaction
        fields = ("first_name", "last_name", "email", "affiliation")

    def save(self, commit=True):
        # do something with self.cleaned_data['rental_vin']
        return super(CustomerForm, self).save(commit=commit)

    def clean(self):
        return self.cleaned_data


class TaskForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('service_description', 'cost', 'amount_paid',)


class RentalForm(ModelForm):
    class Meta:
        model = RentalBike
        fields = ('vin',)


class RefurbishedForm(ModelForm):
    class Meta:
        model = RefurbishedBike
        fields = ('vin',)


class RevenueForm(ModelForm):
    class Meta:
        model = RevenueUpdate


class PartCategoryForm(ModelForm):
    class Meta:
        model = PartCategory
        exclude = ['transaction', 'date_submitted', ]


class DisabledPartCategoryForm(PartCategoryForm):
    class Meta:
        model = PartCategory
        exclude = ['transaction', 'date_submitted', ]
        widgets = {
            'category': forms.Select(attrs={'disabled': 'True'}),
            'price': forms.NumberInput(attrs={'disabled': 'True'}),
            'description': forms.TextInput(attrs={'disabled': 'True'}),
            'was_used': forms.CheckboxInput(attrs={'disabled': 'True'}),
        }


class PartOrderForm(ModelForm):
    class Meta:
        model = PartOrder
        exclude = ['date_submitted', ]

